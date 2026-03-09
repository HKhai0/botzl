from zlapi.models import *
from zlapi import Message, ThreadType
from config import PREFIX, ADMIN

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Xoá tin nhắn người dùng"
}

def handle_go_command(message, message_object, thread_id, thread_type, author_id, client):
    if author_id not in ADMIN:
        noquyen = "Bạn không có quyền để thực hiện điều này!"
        client.replyMessage(Message(text=noquyen), message_object, thread_id, thread_type)
        return

    if message_object.quote:
        msg2del = message_object.quote
        user_id = str(msg2del.ownerId)
    else:
        client.replyMessage(Message(text="Vui lòng reply tin nhắn cần xóa!"), message_object, thread_id, thread_type)
        return

    if msg2del:  
        deleted_msg = client.deleteGroupMsg(msg2del.globalMsgId, user_id, msg2del.cliMsgId, thread_id)
        if deleted_msg.status == 0:
            client.replyMessage(Message(text="Đã xóa tin nhắn thành công!"), message_object, thread_id, thread_type)
        else:
            client.replyMessage(Message(text="Không thể xóa tin nhắn, vui lòng thử lại sau!"), message_object, thread_id, thread_type)
    else:
        client.replyMessage(Message(text="Không thể xóa tin nhắn, vui lòng thử lại sau!"), message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'go': handle_go_command
    }
