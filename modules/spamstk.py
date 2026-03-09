from zlapi.models import *
import time
import threading
from zlapi.models import MessageStyle
from config import ADMIN

is_spamstk_running = False

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Chửi chết cụ 1 con chó"
}

def stop_spamstk(client, message_object, thread_id, thread_type):
    global is_spamstk_running
    is_spamstk_running = False
    client.replyMessage(Message(text="Đã dừng spam sticker."), message_object, thread_id, thread_type)

def handle_spamstk_command(message, message_object, thread_id, thread_type, author_id, client):
    global is_spamstk_running

    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="Bạn không có quyền sử dụng lệnh này."),
            message_object, thread_id, thread_type
        )
        return

    command_parts = message.split()
    if len(command_parts) < 2:
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh hợp lệ (vd: spamstk on hoặc spamstk stop)."), message_object, thread_id, thread_type)
        return

    action = command_parts[1].lower()

    if action == "stop":
        if not is_spamstk_running:
            client.replyMessage(
                Message(text="⚠️ Spam sticker đã dừng trước đó."),
                message_object, thread_id, thread_type
            )
        else:
            stop_spamstk(client, message_object, thread_id, thread_type)
        return

    if action != "on":
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh 'on' hoặc 'stop'."), message_object, thread_id, thread_type)
        return

    is_spamstk_running = True
    def spamstk_loop():
        while is_spamstk_running:
            client.sendSticker(
                stickerType=7,
                stickerId=23339,
                cateId=10425,
                thread_id=thread_id,
                thread_type=thread_type
            )
            time.sleep(0.2)

    spam_thread = threading.Thread(target=spamstk_loop)
    spam_thread.start()

def get_mitaizl():
    return {
        'spamstk': handle_spamstk_command
    }
