import os
import requests
from config import ADMIN
from zlapi.models import Message
import urllib.parse

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Đức Tài",
    'description': "note text"
}

def handle_note_command(message, message_object, thread_id, thread_type, author_id, client):
    text = message.split()

    if len(text) < 2:
        error_message = Message(text="Vui lòng nhập text cần cho vào link note.")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    content = " ".join(text[1:])
    
    if content.startswith("`") and content.endswith("`"):
        formatted_content = f"<pre><code>{content[1:-1]}</code></pre>"
    else:
        formatted_content = content
    
    try:
        data = {
            "status": 200,
            "content": formatted_content,
            "content_type": "application/json",
            "charset": "UTF-8",
            "secret": "mitai project",
            "expiration": "never"
        }

        response = requests.post("https://api.mocky.io/api/mock", json=data)
        response_data = response.json()

        mock_url = response_data.get("link")

        if mock_url:
            response_message = f"Thành công ✅\nDưới đây là link note text của bạn:\nLink: {mock_url}"
        else:
            response_message = "Không thể tạo link note."

    except Exception as e:
        response_message = f"Có lỗi xảy ra: {str(e)}"

    message_to_send = Message(text=response_message)
    client.replyMessage(message_to_send, message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'note': handle_note_command
    }
