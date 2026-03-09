import os
import requests
from config import ADMIN
from zlapi.models import Message

ADMIN_ID = ADMIN

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Áp dụng code từ mọi link raw"
}

def is_admin(author_id):
    return author_id in ADMIN_ID

def read_command_content(command_name):
    try:
        file_path = f"modules/{command_name}.py"
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return str(e)

def save_command_content(command_name, content):
    try:
        file_path = f"modules/{command_name}.py"
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True, None
    except Exception as e:
        return False, str(e)

def fetch_code_from_link(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        return response.text, None
    except Exception as e:
        return None, str(e)

def create_mock_link(code_content):
    try:
        data = {
            "status": 200,
            "content": code_content,
            "content_type": "application/json",
            "charset": "UTF-8",
            "secret": "Kaito Kid",
            "expiration": "never"
        }
        response = requests.post("https://api.mocky.io/api/mock", json=data)
        response_data = response.json()
        return response_data.get("link"), None
    except Exception as e:
        return None, str(e)

def handle_adc_command(message, message_object, thread_id, thread_type, author_id, client):
    sender_name = client.fetchUserInfo(author_id).changed_profiles[author_id].displayName
    if not is_admin(author_id) and sender_name != "Hiển":
        noquyen = "Bạn không có quyền để thực hiện điều này!"
        client.replyMessage(Message(text=noquyen), message_object, thread_id, thread_type)
        return
    
    lenhcanlay = message.split()
    response_message = ""

    if len(lenhcanlay) < 2:
        error_message = Message(text="Vui lòng nhập tên lệnh cần lấy, cập nhật hoặc thêm.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    command_name = lenhcanlay[1].strip()

    if len(lenhcanlay) == 2:
        command_content = read_command_content(command_name)
        if command_content is None:
            response_message = f"Lệnh '{command_name}' không tồn tại."
        else:
            mock_url, error = create_mock_link(command_content)
            if error:
                response_message = f"Có lỗi khi tạo link runmocky: {error}"
            else:
                desc = f"Dưới đây là link và file lệnh '{command_name}'"
                title = "BOT MITAIZL-PROJECT"
                domain_url = "MITAI-PROJECT.VN.COM"
                thumbnail_url = "https://f55-zpg-r.zdn.vn/jpg/7596086360347561851/3bf681fca8ac13f24abd.jpg"
                client.sendLink(
                    linkUrl=mock_url,
                    title=title,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    domainUrl=domain_url,
                    desc=desc,
                    thumbnailUrl=thumbnail_url
                )
                client.sendRemoteFile(
                    fileUrl=mock_url,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    fileName=f"{command_name}.py",
                    fileSize=None,
                    extension="PY"
                )
    elif len(lenhcanlay) == 3:
        runmocky_link = lenhcanlay[2].strip()

        if not is_admin(author_id):
            response_message = "Bạn không đủ quyền hạn để sử dụng lệnh này."
        else:
            code_content, error = fetch_code_from_link(runmocky_link)
            if error:
                response_message = f"Có lỗi khi lấy code từ link: {error}"
            else:
                save_success, error = save_command_content(command_name, code_content)
                if not save_success:
                    response_message = f"Có lỗi khi cập nhật lệnh '{command_name}': {error}"
                else:
                    response_message = f"Đã cập nhật lệnh '{command_name}' thành công. Vui lòng khởi động lại bot để chạy lệnh mới."

    else:
        error_message = Message(text="Cú pháp không hợp lệ. Vui lòng kiểm tra lại.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    if response_message:
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'adc': handle_adc_command
    }
