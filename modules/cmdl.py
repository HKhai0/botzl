import os
import requests
from config import ADMIN
from zlapi.models import Message

ADMIN_ID = ADMIN

des = {
    'version': "1.0.3",
    'credits': "Nguyễn Đức Tài",
    'description': "Quản lý commands"
}

def is_admin(author_id):
    return author_id == ADMIN_ID

def handle_cmdl_command(message, message_object, thread_id, thread_type, author_id, client):
    lenhcanlay = message.split()

    if len(lenhcanlay) < 3:
        error_message = Message(text="Cú pháp không hợp lệ. Vui lòng nhập lệnh đúng.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    command_action = lenhcanlay[1].strip()
    command_name = lenhcanlay[2].strip()

    if command_action == "del":
        if not is_admin(author_id):
            response_message = "Bạn không đủ quyền hạn để sử dụng lệnh này."
            message_to_send = Message(text=response_message)
            client.replyMessage(message_to_send, message_object, thread_id, thread_type)
            return

        file_path = f"modules/{command_name}.py"
        
        if os.path.exists(file_path):
            os.remove(file_path)
            response_message = f"Lệnh '{command_name}' đã được xóa."
        else:
            response_message = f"Lệnh '{command_name}' không tồn tại."

    elif command_action == "rename":
        if len(lenhcanlay) < 4:
            error_message = Message(text="Vui lòng cung cấp tên mới cho lệnh.")
            client.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        new_command_name = lenhcanlay[3].strip()

        if not is_admin(author_id):
            response_message = "Bạn không đủ quyền hạn để sử dụng lệnh này."
            message_to_send = Message(text=response_message)
            client.replyMessage(message_to_send, message_object, thread_id, thread_type)
            return

        old_file_path = f"modules/{command_name}.py"
        new_file_path = f"modules/{new_command_name}.py"

        if os.path.exists(old_file_path):
            os.rename(old_file_path, new_file_path)
            response_message = f"Lệnh '{command_name}' đã được đổi tên thành '{new_command_name}'."
        else:
            response_message = f"Lệnh '{command_name}' không tồn tại."

    else:
        response_message = "Cú pháp không hợp lệ. Vui lòng sử dụng 'del' hoặc 'rename'."

    message_to_send = Message(text=response_message)
    client.replyMessage(message_to_send, message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'cmdl': handle_cmdl_command
    }
