import os
import json
import time
import random
import requests
from zlapi.models import Message
from datetime import datetime
from config import ADMIN

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Đinh Tiến Dũng",
    'description': "Chia sẻ bài viết ảo Facebook"
}

TOKEN_FILE = 'modules/cache/token.json'
HEADERS = {
    'authority': 'graph.facebook.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'upgrade-insecure-requests': '1'
}

def load_tokens():
    """Load tokens from the token file."""
    if not os.path.exists(TOKEN_FILE):
        return []
    with open(TOKEN_FILE, 'r') as f:
        return json.load(f)

def share_post(id_post, quantity, delay, privacy, client, thread_id, thread_type):
    tokens = load_tokens()
    if not tokens:
        client.sendMessage(Message(text="Không tìm thấy token. Vui lòng kiểm tra file token."), thread_id, thread_type)
        return
    
    success_count = 0
    failed_count = 0

    for _ in range(quantity):
        token = random.choice(tokens)
        try:
            url = f"https://graph.facebook.com/me/feed"
            payload = {
                "link": f"https://m.facebook.com/{id_post}",
                "published": 0,
                "privacy": json.dumps({"value": "EVERYONE" if privacy == 1 else "SELF"}),
                "access_token": token
            }
            response = requests.post(url, headers=HEADERS, data=payload)
            response.raise_for_status()

            success_count += 1
            print(f"[SUCCESS] {success_count}/{quantity} - Token: {token} - Time: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            failed_count += 1
            error_message = str(e)
            print(f"[FAILED] Token: {token} - Error: {error_message} - Time: {datetime.now().strftime('%H:%M:%S')}")
            if "OAuthException" in error_message:
                print("Token hết hạn, vui lòng thay token mới.")
        
        time.sleep(delay / 1000)

    client.sendMessage(
        Message(text=f"Hoàn thành chia sẻ!\nSố lần thành công: {success_count}\nSố lần thất bại: {failed_count}"),
        thread_id, thread_type
    )

def handle_shareao_command(message, message_object, thread_id, thread_type, author_id, client):
    params = message.split()
    if len(params) != 5:
        client.sendMessage(
            Message(text="Cú pháp không hợp lệ. Vui lòng sử dụng: shareao <id bài viết>|<số lần>|<số giây>|<quyền riêng tư (1 là công khai, 2 là riêng tư)>"),
            thread_id, thread_type
        )
        return

    try:
        id_post, quantity, delay, privacy = params[1].split('|')
        quantity = int(quantity)
        delay = int(delay)
        privacy = int(privacy)

        if privacy not in [1, 2]:
            raise ValueError("Quyền riêng tư không hợp lệ.")

        client.sendMessage(
            Message(text=f"Đang thực hiện chia sẻ bài viết {id_post}...\nSố lần: {quantity}, Thời gian chờ: {delay}ms, Quyền riêng tư: {'Công khai' if privacy == 1 else 'Riêng tư'}"),
            thread_id, thread_type
        )
        share_post(id_post, quantity, delay, privacy, client, thread_id, thread_type)

    except ValueError as ve:
        client.sendMessage(
            Message(text=f"Lỗi: {str(ve)}"),
            thread_id, thread_type
        )
    except Exception as e:
        client.sendMessage(
            Message(text=f"Có lỗi xảy ra: {str(e)}"),
            thread_id, thread_type
        )

def get_mitaizl():
    return {
        'shareao': handle_shareao_command
    }
