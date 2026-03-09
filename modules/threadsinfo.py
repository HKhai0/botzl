from zlapi.models import Message
import requests
import os

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Lấy thông tin Threads từ username"
}

def handle_threadsinfo_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 2:
        error_message = Message(text="Vui lòng nhập một username Threads hợp lệ.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    username = content[1].strip()

    api_url = f'https://api.mxhgiare.net/threads/info?user={username}'

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if not data:
            error_message = Message(text="Không tìm thấy thông tin Threads cho username đã cung cấp.")
            client.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        fullname = data.get('Fullname', 'Không có thông tin')
        linkacc = data.get('Link', 'Không có thông tin')
        uidacc = data.get('Id', 'Không có thông tin')
        usernameacc = data.get('Username', 'Không có thông tin')
        followers = data.get('Followers', 'Không có thông tin')
        bio = data.get('Bio', 'Không có thông tin')
        avatar = data.get('Avatar', '')
        verified = "Đã xác minh" if data.get('IsVerified') else "Chưa xác minh"
        total_videos = data.get('TotalVideos', 'Không có thông tin')
        total_likes = data.get('TotalLikes', 'Không có thông tin')
        external_links = data.get('ExternalLinks', 'Không có thông tin')
        posts = data.get('Posts', 'Không có thông tin')

        guimess = (
            f"• Tên Threads: {fullname}\n"
            f"• Link Threads: {linkacc}\n"
            f"• UID Threads: {uidacc}\n"
            f"• Username: {usernameacc}\n"
            f"• Người theo dõi: {followers}\n"
            f"• Tiểu sử: {bio}\n"
            f"• Xác minh: {verified}\n"
            f"• Tổng video: {total_videos}\n"
            f"• Tổng lượt thích: {total_likes}\n"
            f"• Liên kết ngoài: {external_links}\n"
            f"• Số bài viết: {posts}"
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
        'threadsinfo': handle_threadsinfo_command
    }