import sys, os
from config import ADMIN
from zlapi.models import Message, MultiMsgStyle, MessageStyle

ADMIN_ID = ADMIN

des = {
    'version': "1.0.0",
    'credits': "Đức Tài",
    'description': "Restart lại bot"
}

def is_admin(author_id):
    return author_id == ADMIN_ID

def handle_reset_command(message, message_object, thread_id, thread_type, author_id, client):
    if not is_admin(author_id):
        noquyen = "Bạn không có quyền để thực hiện điều này!"
        client.replyMessage(Message(text=noquyen), message_object, thread_id, thread_type)
        return
    
    try:
        msg = f"• KHOATDE PROJECT RESTART! \n• Please Wait 5 -> 8 seconds"
        styles = MultiMsgStyle([
            MessageStyle(offset=0, length=2, style="color", color="#a24ffb", auto_format=False),
            MessageStyle(offset=2, length=len(msg) - 2, style="color", color="#ffaf00", auto_format=False),
            MessageStyle(offset=0, length=40, style="color", color="#a24ffb", auto_format=False),
            MessageStyle(offset=45, length=len(msg) - 2, style="color", color="#ffaf00", auto_format=False),
            MessageStyle(offset=0, length=len(msg), style="font", size="13", auto_format=False)
        ])
        client.replyMessage(Message(text=msg, style=styles), message_object, thread_id, thread_type, ttl=5000)
        
        python = sys.executable
        os.execl(python, python, *sys.argv)

    except Exception as e:
        error_msg = f"Lỗi xảy ra khi restart bot: {str(e)}"
        client.replyMessage(Message(text=error_msg), message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'restart': handle_reset_command
    }
