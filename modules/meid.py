from zlapi.models import Message

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Lấy id zalo người dùng hoặc id người được tag"
}

def handle_meid_command(message, message_object, thread_id, thread_type, author_id, client):
    if message_object.mentions:
        tagged_users = message_object.mentions[0]['uid']
    else:
        tagged_users = author_id

    response_message = f"{tagged_users}"

    message_to_send = Message(text=response_message)
    client.replyMessage(message_to_send, message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'meid': handle_meid_command
    }
