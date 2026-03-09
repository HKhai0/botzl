from zlapi.models import Message, Mention
from config import ADMIN

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Đức Tài",
    'description': "Thông báo cho nhóm"
}

def handle_tagall_command(message, message_object, thread_id, thread_type, author_id, client):
    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="🚫 **Bạn không có quyền để thực hiện điều này!**"),
            message_object, thread_id, thread_type
        )
        return

    noidung = message.split()
    
    if len(noidung) < 2:
        error_message = Message(text="Vui lòng nhập nội dung cần thông báo.")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    noidung1 = " ".join(noidung[1:])
    mention = Mention("-1", length=len(noidung1), offset=0)

    content = f"{noidung1}"
    
    client.replyMessage(
        Message(
            text=content, mention=mention
        ),
        message_object,
        thread_id=thread_id,
        thread_type=thread_type
    )

def get_mitaizl():
    return {
        'tagall': handle_tagall_command
    }
