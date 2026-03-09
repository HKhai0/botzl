from zlapi.models import *
from zlapi import Message, ThreadType
from config import PREFIX, ADMIN

des = {
    'version': "1.0.2",
    'credits': "TRBAYK (NGSON)",
    'description': "Xoá tin nhắn người dùng"
}

def handle_go_command(message, message_object, thread_id, thread_type, author_id, client):
    if author_id not in ADMIN:
        noquyen = "Bạn không có quyền để thực hiện điều này!"
        client.replyMessage(Message(text=noquyen), message_object, thread_id, thread_type)
        return
    num_to_delete = 50
    try:
        group_data = client.getRecentGroup(thread_id)

        if not group_data or not hasattr(group_data, 'groupMsgs'):
            client.replyMessage(Message(text="Không có tin nhắn nào để xóa!"), message_object, thread_id, thread_type)
            return
        
        messages_to_delete = group_data.groupMsgs
        if not messages_to_delete:
            client.replyMessage(Message(text="Không có tin nhắn nào để xóa!"), message_object, thread_id, thread_type)
            return

    except Exception as e:
        client.replyMessage(Message(text=f"Lỗi khi lấy tin nhắn: {str(e)}"), message_object, thread_id, thread_type)
        return
    if len(messages_to_delete) < num_to_delete:
        client.replyMessage(Message(text=f"Chỉ có {len(messages_to_delete)} tin nhắn để xóa."), message_object, thread_id, thread_type)
        num_to_delete = len(messages_to_delete)
    deleted_count = 0
    failed_count = 0
    for i in range(num_to_delete):
        msg = messages_to_delete[-(i + 1)]
        print(f"Đang cố gắng xóa tin nhắn: {msg['msgId']}, UID: {msg['uidFrom']}, Nội dung: {msg['content']}, Trạng thái: {msg['status']}")

        user_id = str(msg['uidFrom']) if msg['uidFrom'] != '0' else author_id 
        try:
            deleted_msg = client.deleteGroupMsg(msg['msgId'], user_id, msg['cliMsgId'], thread_id)
            if deleted_msg.status == 0:
                deleted_count += 1
            else:
                failed_count += 1
                print(f"Không thể xóa tin nhắn với ID {msg['msgId']}. Trạng thái trả về: {deleted_msg.status}")
        except Exception as e:
            failed_count += 1
            print(f"Lỗi khi xóa tin nhắn với ID {msg['msgId']}: {str(e)}")
            continue
    if failed_count > 0:
        client.replyMessage(
            Message(text=f"Đã xóa {deleted_count} tin nhắn. Không thể xóa {failed_count} tin nhắn."),
            message_object, thread_id, thread_type
        )
    else:
        client.replyMessage(Message(text=f"Đã xóa {deleted_count} tin nhắn thành công!"), message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'cc': handle_go_command
    }