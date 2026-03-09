from zlapi.models import Message
from config import ADMIN
import sys, os

des = {
    'version': "1.0.0",
    'credits': "t",
    'description': "Kill process của bot"
}

def is_admin(author_id):
    return author_id == ADMIN

def handle_killproc_command(message, message_object, thread_id, thread_type, author_id, client):
    if not is_admin(author_id):
        noquyen = "Bạn không có quyền để thực hiện điều này!"
        client.replyMessage(Message(text=noquyen), message_object, thread_id, thread_type)
        return
    else:
        message_to_send = Message(text="Killing bot process , You need to access the terminal to turn on bot again")
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
    try:
        os.kill(os.getpid(), 9)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
def get_mitaizl():
    return {
        'killproc': handle_killproc_command
    }