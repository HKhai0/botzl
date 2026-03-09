from zlapi.models import Message
import requests
import os

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Lấy thông tin youtube từ link ytb"
}

def handle_ytbinfo_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 2:
        error_message = Message(text="Vui lòng nhập một đường link YouTube hợp lệ.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    linkytb = content[1].strip()

    if not linkytb.startswith("https://"):
        error_message = Message(text="Vui lòng nhập link YouTube hợp lệ!")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    apiuid = f'https://api.mxhgiare.net/channel_id?link={linkytb}'

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(apiuid, headers=headers)
        response.raise_for_status()

        data = response.json()
        channel_id = data.get('channel_id')

        if not channel_id:
            error_message = Message(text="Không tìm thấy Channel ID từ link YouTube đã cung cấp.")
            client.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        getinfo = f'https://api.mxhgiare.net/youtube/info?channel_id={channel_id}'
        response = requests.get(getinfo, headers=headers)
        response.raise_for_status()

        data = response.json()

        title = data.get('title', 'Không có thông tin')
        description = data.get('description', 'Không có thông tin')
        subscriber_count = data.get('subscriber_count', 'Không có thông tin')
        view_count = data.get('view_count', 'Không có thông tin')
        creation_date = data.get('creation_date', 'Không có thông tin')
        avatar = data.get('avatar', {}).get('url', '')
        banner = data.get('banner', {}).get('url', '')

        guimess = (
            f"• Tiêu đề: {title}\n"
            f"• Mô tả: {description}\n"
            f"• Số người đăng ký: {subscriber_count}\n"
            f"• Lượt xem: {view_count}\n"
            f"• Ngày tạo kênh: {creation_date}"
        )
        sendtn = Message(text=guimess)

        gui = Message(text="Avatar của kênh")

        if banner:
            banner_response = requests.get(banner, headers=headers)
            banner_path = 'modules/cache/temp_banner.jpeg'

            with open(banner_path, 'wb') as f:
                f.write(banner_response.content)

            client.sendLocalImage(
                banner_path,
                message=sendtn,
                thread_id=thread_id,
                thread_type=thread_type,
                width=2276,
                height=377
            )

            os.remove(banner_path)

        if avatar:
            avatar_response = requests.get(avatar, headers=headers)
            avatar_path = 'modules/cache/temp_avatar.jpeg'

            with open(avatar_path, 'wb') as f:
                f.write(avatar_response.content)

            client.sendLocalImage(
                avatar_path,
                message=gui,
                thread_id=thread_id,
                thread_type=thread_type,
                width=160,
                height=160
            )

            os.remove(avatar_path)
        else:
            client.sendMessage(sendtn, thread_id, thread_type)

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'ytbinfo': handle_ytbinfo_command
    }