from zlapi.models import Message, Mention
from config import ADMIN
import time

ADMIN_ID = ADMIN

des = {
    'version': "1.0.1",
    'credits': "Đức Tài",
    'description': "Kick toàn bộ thành viên trong nhóm"
}

def is_admin(author_id):
    return author_id == ADMIN_ID

def handle_kickall_command(message, message_object, thread_id, thread_type, author_id, client):
    if not is_admin(author_id):
        response_message = "• Bạn không đủ quyền hạn để sử dụng lệnh này."
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
        return

    try:
        data = client.fetchGroupInfo(groupId=thread_id)
        members = data['gridInfoMap'][str(thread_id)]['memVerList']
        
        for mem in members:
            user_id = mem.split('_')[0]
            user_name = mem.split('_')[1]
            client.kickUsersInGroup(user_id, thread_id)

        success_message = "• Đã xóa toàn bộ thành viên khỏi nhóm."
        client.send(Message(text=success_message), thread_id=thread_id, thread_type=thread_type)

    except Exception as e:
        error_message = f"lỗi clmm: {str(e)}"
        client.send(Message(text=error_message), thread_id=thread_id, thread_type=thread_type)

def get_mitaizl():
    return {
        'kickallmem': handle_kickall_command
    }
