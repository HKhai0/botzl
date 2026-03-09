import os
from zlapi.models import Message
import requests
import json
import urllib.parse
import io
from PIL import Image, ImageDraw
import subprocess

des = {
    'version': "1.0.0",
    'credits': "Quốc Khánh",
    'description': "Tạo sticker khi reply vào một ảnh hoặc video GIF"
}

def handle_stk_command(message, message_object, thread_id, thread_type, author_id, client):
    if message_object.quote:
        attach = message_object.quote.attach
        if attach:
            try:
                attach_data = json.loads(attach)
            except json.JSONDecodeError:
                client.sendMessage(
                    Message(text="Dữ liệu không hợp lệ."),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                return

            media_url = attach_data.get('hdUrl') or attach_data.get('href')
            if not media_url:
                client.sendMessage(
                    Message(text="Không tìm thấy URL."),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                return

            media_url = media_url.replace("\\/", "/")
            media_url = urllib.parse.unquote(media_url)
            if not is_valid_media_url(media_url):
                print(f"URL không hợp lệ: {media_url}")  
                client.sendMessage(
                    Message(text="URL không phải là ảnh, GIF hoặc video hợp lệ."),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                return
            webp_video_url = convert_video_to_webp(media_url)
            if webp_video_url:
                send_sticker(client, media_url, webp_video_url, thread_id, thread_type)
            else:
                client.sendMessage(
                    Message(text="Không thể chuyển đổi video."),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
        else:
            client.sendMessage(
                Message(text="Không có tệp nào được reply."),
                thread_id=thread_id,
                thread_type=thread_type
            )
    else:
        client.sendMessage(
            Message(text="Hãy reply vào ảnh hoặc video cần tạo sticker."),
            thread_id=thread_id,
            thread_type=thread_type
        )

def is_valid_media_url(url):
    try:
        response = requests.head(url)
        content_type = response.headers.get('Content-Type', '')
        if 'video/' in content_type or 'image/' in content_type:
            return True
        response = requests.get(url, stream=True)
        if response.status_code == 200 and len(response.content) > 0:
            return True
        
    except requests.RequestException as e:
        print(f"Lỗi khi kiểm tra URL: {e}")
    
    return False

def convert_video_to_webp(video_url):
    try:
        response = requests.get(video_url)
        if response.status_code != 200:
            print("Không thể tải video:", response.status_code)
            return None
        
        with open("temp.mp4", "wb") as temp_file:  
            temp_file.write(response.content)

        subprocess.run(['ffmpeg', '-y', '-i', 'temp.mp4', '-vcodec', 'libwebp', '-loop', '0', '-q:v', '60', 'output.webp'], check=True)

        with open("output.webp", "rb") as buffered:
            webp_video_url = upload_to_catbox(buffered)

        os.remove("temp.mp4")
        os.remove("output.webp")

        return webp_video_url

    except subprocess.CalledProcessError as e:
        print(f"Lỗi trong quá trình chuyển đổi video: {e}")
    except Exception as e:
        print("Lỗi trong quá trình chuyển đổi video:", e)
    return None

def upload_to_catbox(buffered):
    url = "https://catbox.moe/user/api.php"
    
    files = {
        'fileToUpload': ('image.webp', buffered, 'image/webp')
    }
    
    data = {
        'reqtype': 'fileupload'
    }
    
    response = requests.post(url, files=files, data=data)

    print("Nội dung phản hồi từ Catbox:", response.text)  

    if response.status_code == 200 and response.text.startswith("http"):
        return response.text  
    else:
        print("Lỗi khi upload:", response.text)
    
    return None

def send_sticker(client, staticImgUrl, animationImgUrl, thread_id, thread_type):
    try:
        client.sendCustomSticker(
            staticImgUrl=staticImgUrl,
            animationImgUrl=animationImgUrl,
            thread_id=thread_id,
            thread_type=thread_type
        )
        
    except Exception as e:
        client.sendMessage(
            Message(text=f"Không thể gửi sticker: {str(e)}"),
            thread_id=thread_id,
            thread_type=thread_type
        )

def get_mitaizl():
    return {
        'stk': handle_stk_command
    }