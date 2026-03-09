import re
from zlapi.models import Message
from config import ADMIN

des = {
    'version': "1.0.1",
    'credits': "Nguyễn Đức Tài",
    'description': "Gửi liên kết đến người dùng hoặc nhóm với hình ảnh tùy chỉnh"
}

url_pattern = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)

def send_link(message, message_object, thread_id, thread_type, author_id, client):
    parts = message.split('|')
    if len(parts) < 5:
        client.sendMessage(
            Message(text="🚫 **Cú pháp không chính xác!** Vui lòng nhập: sendlink <link>|<link ảnh nền>|<title>|<domain>|<des>."),
            thread_id, thread_type
        )
        return

    possible_urls = re.findall(url_pattern, parts[0])
    if not possible_urls:
        client.sendMessage(
            Message(text="🚫 **Không tìm thấy URL hợp lệ!** Vui lòng cung cấp một URL hợp lệ."),
            thread_id, thread_type
        )
        return

    link_url = possible_urls[0].strip()
    thumbnail_url = parts[1].strip()
    title = parts[2].strip()
    domain_url = parts[3].strip()
    desc = parts[4].strip()

    client.sendLink(
        linkUrl=link_url,
        title=title,
        thread_id=thread_id,
        thread_type=thread_type,
        domainUrl=domain_url,
        desc=desc,
        thumbnailUrl=thumbnail_url
    )

def get_mitaizl():
    return {
        'sendlink': send_link
    }
