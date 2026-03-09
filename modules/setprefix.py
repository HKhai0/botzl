import json
from zlapi.models import Message
from config import ADMIN

des = {
    'version': "1.0.6",
    'credits': "Nguyễn Đức Tài",
    'description': "Đổi prefix"
}
def is_admin(author_id):
    return author_id == ADMIN

def prf():
    with open('seting.json', 'r') as f:
        return json.load(f).get('prefix')

def set_new_prefix(new_prefix):
    with open('seting.json', 'r') as f:
        data = json.load(f)

    data['prefix'] = new_prefix

    with open('seting.json', 'w') as f:
        json.dump(data, f, indent=4)

def handle_setprefix_command(message, message_object, thread_id, thread_type, author_id, client):
    if not is_admin(author_id):
        response_message = "• Bạn không đủ quyền hạn để sử dụng lệnh này."
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
        return

    text = message.split()

    if len(text) < 2:
        error_message = Message(text="Vui lòng nhập prefix mới")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    new_prefix = text[1]
    set_new_prefix(new_prefix)  # Gọi hàm để lưu prefix mới
    success_message = Message(text=f"Prefix đã được đổi thành: {new_prefix}")
    client.replyMessage(success_message, message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'setprefix': handle_setprefix_command
    }
