from zlapi.models import Message
from config import ADMIN
import time

des = {
    'version': "1.2.0",
    'credits': "Nguyễn Đức Tài x TRBAYK",
    'description': "Kick và thêm lại thành viên vào nhóm nhiều lần bằng UID hoặc số điện thoại."
}

def handle_addkick_command(message, message_object, thread_id, thread_type, author_id, client):
    text = message.split()

    if len(text) < 3:  # Đảm bảo rằng lệnh bao gồm ít nhất 3 phần: lệnh, user_id và số lần lặp
        error_message = Message(text="Vui lòng sử dụng cú pháp: .addkick @tag hoặc .addkick <ID> <số lần lặp>.")
        client.sendMessage(error_message, thread_id, thread_type,ttl=10000)
        return

    user_id = None
    repeat_count = 1  # Số lần lặp mặc định là 1

    # Lấy user_id từ tag, quote hoặc ID được nhập
    if message_object.mentions:
        user_id = message_object.mentions[0]['uid']
    elif message_object.quote:
        user_id = str(message_object.quote.ownerId)
    else:
        user_id = text[1]

    # Kiểm tra số lần lặp lại
    try:
        repeat_count = int(text[2])
        if repeat_count < 1:
            repeat_count = 1  # Nếu số lần lặp không hợp lệ, đặt lại thành 1
    except ValueError:
        client.sendMessage(Message(text="Số lần lặp không hợp lệ."), thread_id, thread_type,ttl=10000)
        return

    # Kiểm tra quyền admin của người gửi lệnh
    group_info = client.fetchGroupInfo(thread_id)
    if not group_info:
        client.sendMessage(Message(text="Không thể lấy thông tin nhóm."), thread_id, thread_type,ttl=10000)
        return

    group_data = group_info.gridInfoMap.get(thread_id)
    if not group_data:
        client.sendMessage(Message(text="Không tìm thấy thông tin nhóm."), thread_id, thread_type,ttl=10000)
        return

    creator_id = group_data.get('creatorId')
    admin_ids = group_data.get('adminIds', [])
    all_admin_ids = set(admin_ids)
    all_admin_ids.add(creator_id)
    all_admin_ids.update(ADMIN)

    if author_id not in all_admin_ids and author_id not in ADMIN:
        client.sendMessage(Message(text="Bạn không có quyền thực hiện hành động này!"), thread_id, thread_type,ttl=10000)
        return

    for i in range(repeat_count):
        # Thực hiện kick người dùng
        try:
            client.kickUsersInGroup(user_id, thread_id)
            send_message = f""
            # send_message = f"Đã sút thành công {user_id} ra khỏi nhóm."
            client.sendMessage(Message(text=send_message), thread_id, thread_type)
        except Exception as e:
            client.sendMessage(Message(text=f"Lỗi khi sút người dùng: {str(e)}"), thread_id, thread_type,ttl=10000)
            return

        # Thêm lại người dùng sau khi kick
        try:
            time.sleep(0.5)  # Đợi 2 giây trước khi thêm lại

            client.addUsersToGroup(user_id, thread_id)

            user_info = client.fetchUserInfo(user_id)
            if isinstance(user_info, dict) and 'changed_profiles' in user_info:
                user_data = user_info['changed_profiles'].get(user_id, {})
                user_name = user_data.get('zaloName', 'Không rõ tên.')
            else:
                user_name = "Người dùng không rõ tên."

            send_message = f""
            client.sendMessage(Message(text=send_message), thread_id, thread_type,ttl=10000)
        except Exception as e:
            client.sendMessage(Message(text=f"Lỗi khi thêm lại người dùng: {str(e)}"), thread_id, thread_type,ttl=10000)
            return

def get_mitaizl():
    return {
        'addkick': handle_addkick_command
    }
#  send_message = f"({i+1}/{repeat_count}) Đã thêm lại thành công {user_name} vào nhóm."