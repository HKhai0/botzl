import os
import json
import requests
import mimetypes
import urllib.parse
from zlapi.models import Message
from config import ADMIN

def is_admin(author_id):
    return author_id == ADMIN

des = {
    'version': "1.0.0",
    'credits': "NGSON(TRBAYK)",
    'description': "Để tải ảnh hoặc video và lưu link vào file JSON."
}

def handle_data_command(message, message_object, thread_id, thread_type, author_id, client):
    if not is_admin(author_id):
        client.replyMessage(
            Message(text="• Bạn không đủ quyền hạn để sử dụng lệnh này."),
            message_object, thread_id, thread_type
        )
        return

    command_parts = message.split()
    if len(command_parts) < 2:
        client.sendMessage(
            Message(text="Vui lòng cung cấp tên file."),
            thread_id=thread_id, thread_type=thread_type, ttl=1000
        )
        return

    file_name = command_parts[1]
    json_file_path = os.path.join("modules", "cache", "data", f"{file_name}.json")

    if os.path.exists(json_file_path):
        client.sendMessage(
            Message(text=f"Tệp {file_name}.json đã tồn tại. Đang thêm link vào tệp."),
            thread_id=thread_id, thread_type=thread_type, ttl=10000
        )
    else:
        client.sendMessage(
            Message(text=f"Tệp {file_name}.json không tồn tại. Đang tạo mới."),
            thread_id=thread_id, thread_type=thread_type, ttl=20000
        )
        with open(json_file_path, "w") as json_file:
            json.dump([], json_file)

    if message_object.quote and message_object.quote.attach:
        attach = message_object.quote.attach
        try:
            attach_data = json.loads(attach)
            media_url = attach_data.get('hdUrl') or attach_data.get('href')
            if not media_url:
                raise ValueError("Không tìm thấy URL.")
            
            media_url = urllib.parse.unquote(media_url.replace("\\/", "/"))
            content_type = get_content_type(media_url)
            if content_type is None:
                raise ValueError("Không thể xác định loại tệp từ URL.")
            
            file_extension = mimetypes.guess_extension(content_type.split(';')[0])
            local_file_path = f"{file_name}{file_extension}"

            if download_media(media_url, local_file_path):
                uploaded_url = upload_to_catbox(local_file_path)
                if uploaded_url:
                    save_to_json(file_name, uploaded_url)
                    url_count = count_urls_in_json(json_file_path)
                    client.sendMessage(
                        Message(text=f"Lệnh: add {file_name}.py vào api\nĐã thêm link: {uploaded_url} vào {file_name}.json\nSố lượng URL hiện tại: {url_count}"),
                        thread_id=thread_id, thread_type=thread_type, ttl=30000
                    )
                else:
                    client.sendMessage(
                        Message(text="Không thể upload lên Catbox."),
                        thread_id=thread_id, thread_type=thread_type
                    )
                os.remove(local_file_path)
            else:
                client.sendMessage(
                    Message(text="Không thể tải media."),
                    thread_id=thread_id, thread_type=thread_type
                )
        except (json.JSONDecodeError, ValueError) as e:
            client.sendMessage(
                Message(text=str(e)),
                thread_id=thread_id, thread_type=thread_type
            )
    else:
        client.sendMessage(
            Message(text="Vui lòng reply một ảnh hoặc video để thêm."),
            thread_id=thread_id, thread_type=thread_type
        )

def get_content_type(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.headers.get('Content-Type')
    except Exception as e:
        print(f"Đã xảy ra lỗi khi truy cập URL: {e}")
        return None

def download_media(media_url, local_file_path):
    try:
        response = requests.get(media_url)
        if response.status_code == 200:
            with open(local_file_path, "wb") as file:
                file.write(response.content)
            return True
    except Exception as e:
        print(f"Lỗi khi tải media: {e}")
    return False

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    
    with open(file_path, "rb") as buffered:
        files = {'fileToUpload': (os.path.basename(file_path), buffered)}
        data = {'reqtype': 'fileupload'}
        
        try:
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200 and response.text.startswith("http"):
                return response.text  
            else:
                print("Lỗi khi upload:", response.text)
        except Exception as e:
            print(f"Lỗi khi upload: {e}")
    
    return None

def save_to_json(filename, url):
    file_path = f"modules/cache/data/{filename}.json"
    
    with open(file_path, "r+") as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            data = []          
        
        data.append(url)
        
        json_file.seek(0)
        json.dump(data, json_file, indent=4)

def count_urls_in_json(file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return len(data)
        
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def get_mitaizl():
    return {
        'data': handle_data_command
    }
    