import os
import requests
from config import *
from zlapi.models import *

des = {
    "version": "1.0.0",
    "credits": "Nguyễn Đức Tài",
    "description": "Áp dụng code all link raw",
}


def read_command_content(command_name):
    try:
        file_path = f"modules/{command_name}.py"

        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return str(e)


def handle_adc_command(
    message, message_object, thread_id, thread_type, author_id, client
):
    lenhcanlay = message.split()

    if len(lenhcanlay) < 2:
        error_message = Message(text="Vui lòng nhập tên lệnh cần lấy.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    command_name = lenhcanlay[1].strip()
    sender_name = client.fetchUserInfo(author_id).changed_profiles[author_id].displayName
    if not is_admin(author_id) and sender_name != "Hiển":
        print(sender_name)
        ms = "Xin lỗi. Bạn không có quyền sử dụng lệnh này!"
        msg = Message(text=ms)
        client.replyMessage(msg, message_object, thread_id, thread_type, ttl=60000)
        return

    command_content = read_command_content(command_name)

    if command_content is None:
        response_message = (
            f"Lệnh '{command_name}' không được tìm thấy trong thư mục share."
        )
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
        return

    try:
        data = {
            "status": 200,
            "content": command_content,
            "content_type": "application/json",
            "charset": "UTF-8",
            "secret": "Kaito Kid",
            "expiration": "never",
        }

        response = requests.post("https://api.mocky.io/api/mock", json=data)
        response_data = response.json()

        mock_url = response_data.get("link")

        if mock_url:
            response_message = f"Thành công ✅\nDưới đây là link runmocky của lệnh {command_name}\nLink: {mock_url}"
        else:
            response_message = "Không thể tạo link run.mocky."

    except Exception as e:
        response_message = f"Có lỗi xảy ra: {str(e)}"

    message_to_send = Message(text=response_message)
    client.replyMessage(message_to_send, message_object, thread_id, thread_type)


def get_mitaizl():
    return {"share": handle_adc_command}
