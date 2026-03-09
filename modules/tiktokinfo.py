from zlapi.models import Message
import requests
import os

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Lấy thông tin người dùng tiktok từ id"
}

def handle_tiktokinfo_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 2:
        error_message = Message(text="Vui lòng nhập một id tiktok cần lấy thông tin.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    iduser = content[1].strip()

    try:
        api_url = f'https://api.mxhgiare.net/v2/tiktok/tikwm.json?info={iduser}'
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        if data.get('code') != 0:
            raise KeyError("API trả về kết quả không thành công.")

        user = data['data'].get('user', {})
        stats = data['data'].get('stats', {})

        if user:
            uid = user.get('id')
            username = user.get('uniqueId')
            name = user.get('nickname')
            tieusu = user.get('signature')
            lkig = user.get('ins_id', 'Chưa có liên kết nào')
            lkx = user.get('twitter_id', 'Chưa có liên kết nào')
            lkytb = user.get('youtube_channel_title', 'Chưa có liên kết nào')
            avt = user.get('avatarMedium')

            if stats:
                tim = stats.get('heart', 0)
                dangfl = stats.get('followingCount', 0)
                sofl = stats.get('followerCount', 0)
                tongvd = stats.get('videoCount', 0)

                gui = (
                    f"• Tên: {name}\n"
                    f"• Id tiktok: {uid}\n"
                    f"• Username tiktok: {username}\n"
                    f"• Tiểu sử: {tieusu}\n"
                    f"• Số follower: {sofl}\n"
                    f"• Đang follower: {dangfl}\n"
                    f"• Số video đã đăng: {tongvd}\n"
                    f"• Tổng số tim tiktok: {tim}\n"
                    f"• Các liên kết mạng xã hội\n"
                    f"• Instagram: {lkig}\n"
                    f"• Youtube: {lkytb}\n"
                    f"• Twitter: {lkx}"
                )

                messagesend = Message(text=gui)

                if avt:
                    image_response = requests.get(avt)
                    image_path = 'modules/cache/temp_tiktok.jpeg'

                    with open(image_path, 'wb') as f:
                        f.write(image_response.content)

                    client.sendLocalImage(
                        image_path, 
                        message=messagesend,
                        thread_id=thread_id,
                        thread_type=thread_type,
                        width=2500,
                        height=2500
                    )

                    os.remove(image_path)
                else:
                    raise Exception("Không thể gửi ảnh")

            else:
                raise KeyError("Không tìm thấy thông tin thống kê từ API.")
        else:
            raise KeyError("Không tìm thấy thông tin người dùng từ API.")

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except KeyError as e:
        error_message = Message(text=f"Dữ liệu từ API không đúng cấu trúc: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi không xác định: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'tiktokinfo': handle_tiktokinfo_command
    }
