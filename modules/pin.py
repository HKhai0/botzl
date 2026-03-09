import time
from zlapi.models import *
import requests
import urllib.parse
import os

des = {
    'version': "1.9.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Tìm ảnh trên pinterest"
}

user_cooldowns = {}

def handle_pin_command(message, message_object, thread_id, thread_type, author_id, client):
    current_time = time.time()
    cooldown_time = 7 * 60

    if author_id in user_cooldowns:
        time_since_last_use = current_time - user_cooldowns[author_id]
        if time_since_last_use < cooldown_time:
            remaining_time = cooldown_time - time_since_last_use
            error_message = Message(text=f"Bạn phải đợi {int(remaining_time // 60)} phút {int(remaining_time % 60)} giây nữa mới có thể dùng lại lệnh.")
            client.replyMessage(error_message, message_object, thread_id, thread_type)
            return

    user_cooldowns[author_id] = current_time

    text = message.split()

    if len(text) < 2 or not text[1].strip():
        error_message = Message(text="Vui lòng nhập nội dung cần tìm ảnh")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    content = " ".join(text[1:])
    encoded_text = urllib.parse.quote(content, safe='')

    try:
        apianh = f'https://apiquockhanh.click/pinterest?search={encoded_text}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(apianh, headers=headers)
        response.raise_for_status()

        data = response.json()
        c = data.get('count', 0)
        links = data.get('data', [])

        if len(links) == 0:
            error_message = Message(text="Không tìm thấy ảnh nào.")
            client.sendMessage(error_message, thread_id, thread_type)
            return

        image_paths = []
        for idx, link in enumerate(links[:c]):
            if link:
                image_response = requests.get(link, headers=headers)
                image_path = f'modules/cache/temp_image_{idx}.jpeg'
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
                image_paths.append(image_path)

        if all(os.path.exists(path) for path in image_paths):
            total_images = len(image_paths)
            gui = Message(text=f"Đã gửi: {total_images} ảnh")
            client.sendMultiLocalImage(
                imagePathList=image_paths, 
                message=gui,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1600,
                height=1600,
                ttl=200000
            )
            for path in image_paths:
                os.remove(path)
                
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
        'pin': handle_pin_command
    }
