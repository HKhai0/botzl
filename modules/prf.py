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
        noquyen = "This is Admin Only"
        client.sendReaction(messageObject=message_object, reactionIcon=noquyen, thread_id=thread_id, thread_type=thread_type)
        return

    text = message.split()

    if len(text) < 2:
        text = "Please Input Prefix"
        client.sendReaction(messageObject=message_object, reactionIcon=text, thread_id=thread_id, thread_type=thread_type)
        return

    new_prefix = text[1]
    set_new_prefix(new_prefix)  # Gọi hàm để lưu prefix mới
    prf = f"New Prefix: {new_prefix}"
    client.sendReaction(messageObject=message_object, reactionIcon=prf, thread_id=thread_id, thread_type=thread_type)

def get_mitaizl():
    return {
        'prf': handle_setprefix_command
    }
