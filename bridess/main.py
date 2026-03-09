from flask import Flask, request, jsonify
from fbchat_muqit import Client, EventType
from fbchat_muqit.models import Message, MessageUnsend

# initialize fbchat client using cookies file (or credentials)
# adjust path or arguments depending on your setup
client = Client(cookies_file_path="cookies.json")

# placeholder defaults (examples)
DEFAULT_THREADS = [
    "1110661484589826",
    "8114038808696028",
]

# store messages posted before client.loop is ready
pending_messages = []

import threading, time, asyncio

def _flush_pending():
    # run in background, attempt to send queued messages once loop exists
    while True:
        if hasattr(client, 'loop') and client.loop is not None:
            while pending_messages:
                text, tids = pending_messages.pop(0)
                for tid in tids:
                    try:
                        fut = asyncio.run_coroutine_threadsafe(
                            client.send_message(text, thread_id=tid),
                            client.loop
                        )
                        def _cb(f,fid=tid):
                            try:
                                res = f.result()
                                print(f"[bot][pending] sent to {fid}, msg id={res}")
                            except Exception as ex:
                                print(f"[bot][pending] error {fid}: {ex}")
                        fut.add_done_callback(_cb)
                    except Exception as e:
                        print(f"[bot][pending] scheduling failed {tid}: {e}")
        time.sleep(1)

# start flush thread immediately
threading.Thread(target=_flush_pending, daemon=True).start()

# example event handlers (if needed):
# @bot.event(EventType.MESSAGE)
# async def on_message(message: Message):
#     pass

# @bot.event(EventType.MESSAGE_UNSENT)
# async def on_message_unsent(message: MessageUnsend):
#     pass

# flask app stub – sending logic removed for documentation purpose
app = Flask(__name__)

@app.route("/send", methods=["POST"])
def send():
    """Endpoint to receive JSON payload from web service.
    The actual FB sending code was removed as requested; add
    your own implementation here when ready.
    """
    data = request.get_json(force=True)
    print("[bot] received payload for documentation:", data)

    # determine message text and target threads
    text = data.get("message") or str(data)
    thread_ids = data.get("thread_ids", DEFAULT_THREADS)
    if not thread_ids:
        thread_ids = []

    import asyncio
    for tid in thread_ids:
        if not hasattr(client, 'loop') or client.loop is None:
            # queue until loop ready
            print(f"[bot] loop not ready; queueing '{text}' for {tid}")
            pending_messages.append((text, [tid]))
            continue
        try:
            print(f"[bot] scheduling send of '{text}' to {tid}")
            future = asyncio.run_coroutine_threadsafe(
                client.send_message(text, thread_id=tid),
                client.loop
            )
            # optionally check result
            def _cb(fut, tid=tid):
                try:
                    res = fut.result()
                    print(f"[bot] sent to {tid}, msg id={res}")
                except Exception as e:
                    print(f"[bot] send error {tid}: {e}")
            future.add_done_callback(_cb)
        except Exception as e:
            print(f"failed scheduling for {tid}: {e}")
    # ... processing would happen here
    # Example: if you wanted to send a reply and capture its message id,
    # you need to run inside an async context or schedule the coroutine
    # on bot.loop. Here's a demonstration using run_coroutine_threadsafe:
    #
    # text_to_send = "hello back"
    # future = asyncio.run_coroutine_threadsafe(
    #     bot.send_message(text_to_send, thread_id=data.get('thread_id')),
    #     bot.loop
    # )
    # try:
    #     msg_id = future.result(timeout=5)
    #     print("sent message id", msg_id)
    # except Exception as ex:
    #     print("failed to send or capture", ex)
    #
    # In an async handler you could instead write:
    #   msg_id = await bot.send_message(text_to_send, thread_id=...)
    #
    return jsonify({"status": "placeholder"}), 200


    

if __name__ == "__main__":
    # run flask and client concurrently
    import threading
    def run_app():
        app.run(host="0.0.0.0", port=6000)

    threading.Thread(target=run_app, daemon=True).start()
    client.run()
