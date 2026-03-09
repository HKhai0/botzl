from zlapi.models import Message, ThreadType

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Lấy danh thiếp người dùng hoặc danh thiếp người được tag"
}

def handle_cardinfo_command(message, message_object, thread_id, thread_type, author_id, client):

    userId = message_object.mentions[0]['uid'] if message_object.mentions else author_id
    
    if not userId:
        client.send(
            Message(text="Không tìm thấy người dùng."),
            thread_id=thread_id,
            thread_type=thread_type
        )
        return
    
    
    user_info = client.fetchUserInfo(userId).changed_profiles.get(userId)
    
    if not user_info:
        client.send(
            Message(text="Không thể lấy thông tin người dùng."),
            thread_id=thread_id,
            thread_type=thread_type
        )
        return
    
    avatarUrl = user_info.avatar
    
    if not avatarUrl:
        client.send(
            Message(text="Người dùng này không có ảnh đại diện."),
            thread_id=thread_id,
            thread_type=thread_type
        )
        return
    
    client.sendBusinessCard(userId=userId, qrCodeUrl=avatarUrl, thread_id=thread_id, thread_type=thread_type)

def get_mitaizl():
    return {
        'cardinfo': handle_cardinfo_command
    }
