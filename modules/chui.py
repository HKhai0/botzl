from zlapi.models import *
import os
import time
import threading
from zlapi.models import MessageStyle
from config import ADMIN

is_reo_running = False

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Chửi chết cụ 1 con chó"
}

def stop_reo(client, message_object, thread_id, thread_type):
    global is_reo_running
    is_reo_running = False
    client.replyMessage(Message(text="Đã dừng réo."), message_object, thread_id, thread_type)

def handle_chui_command(message, message_object, thread_id, thread_type, author_id, client):
    global is_reo_running

    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="Quyền lồn biẻn giới"),
            message_object, thread_id, thread_type
        )
        return

    command_parts = message.split()
    if len(command_parts) < 2:
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh hợp lệ (vd: chui on hoặc chui stop)."), message_object, thread_id, thread_type)
        return

    action = command_parts[1].lower()

    if action == "stop":
        if not is_reo_running:
            client.replyMessage(
                Message(text="⚠️ **chửi đã dừng lại.**"),
                message_object, thread_id, thread_type
            )
        else:
            stop_reo(client, message_object, thread_id, thread_type)
        return

    if action != "on":
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh 'on' hoặc 'stop'."), message_object, thread_id, thread_type)
        return

    try:
        with open("noidung.txt", "r", encoding="utf-8") as file:
            Ngon = file.readlines()
    except FileNotFoundError:
        client.replyMessage(
            Message(text="Không tìm thấy file noidung.txt."),
            message_object,
            thread_id,
            thread_type
        )
        return

    if not Ngon:
        client.replyMessage(
            Message(text="File noidung.txt không có nội dung nào để gửi."),
            message_object,
            thread_id,
            thread_type
        )
        return

    is_reo_running = True
    def reo_loop():
        while is_reo_running:
            for noidung in Ngon:
                if not is_reo_running:
                    break
                client.send(Message(text=f"{noidung}"), thread_id, thread_type)
                time.sleep(0.4)

    reo_thread = threading.Thread(target=reo_loop)
    reo_thread.start()

def get_mitaizl():
    return {
        'chui': handle_chui_command
    }
