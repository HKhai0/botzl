import os
import requests
from zlapi.models import *
from config import ADMIN

ADMIN_ID = ADMIN

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Đức Tài",
    'description': "Gửi link lệnh đến người được tag"
}

def is_admin(author_id):
    return author_id in ADMIN_ID

def read_command_content(command_name):
    try:
        file_path = f"modules/{command_name}.py"
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return str(e)

def create_mock_link(code_content):
    try:
        data = {
            "status": 200,
            "content": code_content,
            "content_type": "application/json",
            "charset": "UTF-8",
            "secret": "Kaito Kid",
            "expiration": "never"
        }
        response = requests.post("https://api.mocky.io/api/mock", json=data)
        response_data = response.json()
        return response_data.get("link"), None
    except Exception as e:
        return None, str(e)

def handle_sendmdl_command(message, message_object, thread_id, thread_type, author_id, client):
    if not is_admin(author_id):
        noquyen = "Bạn không có quyền để thực hiện điều này!"
        client.replyMessage(Message(text=noquyen), message_object, thread_id, thread_type)
        return

    if message_object.mentions:
        tagged_user_id = message_object.mentions[0]['uid']
    else:
        error_message = "Vui lòng tag người cần gửi lệnh."
        client.replyMessage(Message(text=error_message), message_object, thread_id, thread_type)
        return

    lenhcanlay = message.split()

    if len(lenhcanlay) < 2:
        error_message = Message(text="Vui lòng nhập tên lệnh cần gửi.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    command_name = lenhcanlay[1].strip()
    command_content = read_command_content(command_name)

    if command_content is None:
        response_message = f"Lệnh '{command_name}' không tồn tại."
        client.replyMessage(Message(text=response_message), message_object, thread_id, thread_type)
    else:
        mock_url, error = create_mock_link(command_content)
        if error:
            gui = f"Có lỗi khi tạo link runmocky: {error}"
            client.replyMessage(Message(text=gui), message_object, thread_id, thread_type)
        else:
            author_info = client.fetchUserInfo(tagged_user_id).changed_profiles.get(tagged_user_id, {})
            author_name = author_info.get('zaloName', 'Không xác định')

            gui = f"Gửi lệnh {command_name} thành công đến người dùng: {author_name}"
            client.send(Message(text=gui), thread_id, thread_type)

            gui = f"Dưới đây là link lệnh '{command_name}': {mock_url}"
            client.send(Message(text=gui), tagged_user_id, ThreadType.USER)
            
            client.sendRemoteFile(
                fileUrl=mock_url,
                fileName=f"{command_name}.py",
                thread_id=tagged_user_id,
                thread_type=ThreadType.USER,
                fileSize=None,
                extension="PY"
            )

def get_mitaizl():
    return {
        'sendmdl': handle_sendmdl_command
    }
