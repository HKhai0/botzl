from zlapi.models import Message
import requests
import os

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Lấy thông tin Instagram từ username"
}

def handle_iginfo_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 2:
        error_message = Message(text="Vui lòng nhập một username Instagram hợp lệ.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    username = content[1].strip()

    api_url = f'https://api.mxhgiare.net/instagram/info?username={username}'

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if not data:
            error_message = Message(text="Không tìm thấy thông tin Instagram cho username đã cung cấp.")
            client.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        ten = data.get('fullName', 'Không có thông tin')
        linkacc = data.get('link', 'Không có thông tin')
        uidacc = data.get('id', 'Không có thông tin')
        usernameacc = data.get('username', 'Không có thông tin')
        follower = data.get('followers', 'Không có thông tin')
        following = data.get('following', 'Không có thông tin')
        bio = data.get('bio', 'Không có thông tin')
        bioLinks = data.get('bioLinks', 'Không có thông tin')
        author = data.get('author', 'Không có thông tin')
        avatar = data.get('avatar', '')
        verified = "Đã xác minh" if data.get('isVerified') else "Chưa xác minh"

        guimess = (
            f"• Tên Instagram: {ten}\n"
            f"• Link Instagram: {linkacc}\n"
            f"• UID Instagram: {uidacc}\n"
            f"• Username: {usernameacc}\n"
            f"• Người theo dõi: {follower}\n"
            f"• Đang theo dõi: {following}\n"
            f"• Tiểu sử: {bio}\n"
            f"• Liên kết tiểu sử: {bioLinks}\n"
            f"• Xác minh: {verified}"
        )
        sendtn = Message(text=guimess)

        if avatar:
            image_response = requests.get(avatar, headers=headers)
            image_path = 'modules/cache/temp_image3.jpeg'

            with open(image_path, 'wb') as f:
                f.write(image_response.content)

            client.sendLocalImage(
                image_path, 
                message=sendtn,
                thread_id=thread_id,
                thread_type=thread_type,
                width=2500,
                height=2500
            )

            os.remove(image_path)
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
        'iginfo': handle_iginfo_command
    }