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
        noquyen = "This is Admin Only"
        client.sendReaction(messageObject=message_object, reactionIcon=noquyen, thread_id=thread_id, thread_type=thread_type)
        return
    
    try:
        icon = "🔄Restarting : "
        client.sendReaction(messageObject=message_object, reactionIcon=icon, thread_id=thread_id, thread_type=thread_type)
        icon = "Take Up To 3s"
        client.sendReaction(messageObject=message_object, reactionIcon=icon, thread_id=thread_id, thread_type=thread_type)
        
        python = sys.executable
        os.execl(python, python, *sys.argv)

    except Exception as e:
        error_msg = f"Lỗi xảy ra khi restart bot: {str(e)}"
        client.replyMessage(Message(text=error_msg), message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'rs': handle_reset_command
    }
