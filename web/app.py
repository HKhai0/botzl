from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__, template_folder="templates")

# store received log entries in memory
logs = []

# URL of the fbchat bot service to forward messages to
BOT_URL = "http://localhost:6000/send"

@app.route("/", methods=["GET"])
def index():
    # initial page; JS will pull the latest entries
    return render_template("index.html")

@app.route("/logs", methods=["GET"])
def get_logs():
    # return list of entries as JSON
    return jsonify(logs)

@app.route("/process", methods=["POST"])
def process():
    try:
        data = request.get_json(force=True)
    except Exception:
        data = request.form.to_dict() or request.data.decode('utf-8')

    logs.append(data)
    print("[web] received:", data)
    # forward to fbchat bot service
    try:
        # assume incoming data has "message" field and optionally thread_ids
        requests.post(BOT_URL, json=data, timeout=2)
    except Exception as e:
        print(f"[web] failed to forward to bot: {e}")
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
