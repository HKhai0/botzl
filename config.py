import json
import base64
import os
import re
import os
import json
SETTING_FILE= "seting.json"
#Không chỉnh sửa nếu bạn không có kinh nghiệm
def read_settings():
    """Đọc toàn bộ nội dung từ file JSON."""
    try:
        with open(SETTING_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def write_settings(settings):
    """Ghi toàn bộ nội dung vào file JSON."""
    with open(SETTING_FILE, 'w', encoding='utf-8') as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)


def is_admin(author_id):
    settings = read_settings()
    admin_bot = settings.get("adm", [])
    if author_id in admin_bot:
        return True
    else:
        return False
def get_user_name_by_id(bot,author_id):
    try:
        user = bot.fetchUserInfo(author_id).changed_profiles[author_id].displayName
        return user
    except:
        return "Unknown User"

def handle_bot_admin(bot):
    settings = read_settings()
    admin_bot = settings.get("adm", [])
    if bot.uid not in admin_bot:
        admin_bot.append(bot.uid)
        settings['adm'] = admin_bot
        write_settings(settings)
        print(f"Đã thêm 👑{get_user_name_by_id(bot, bot.uid)} 🆔 {bot.uid} cho lần đầu tiên khởi động vào danh sách Admin 🤖BOT ✅")

settings= read_settings()
ADMIN = [settings.get("adm", [])]
def read_imei():
    with open('dataLogin/imei.txt', 'r') as f:
        imei = f.read().strip()
    return imei

def is_base64_encoded(data):
    try:
        base64.b64decode(data).decode('utf-8')
        return True
    except Exception:
        return False

def read_and_format_cookies():
    encCookie = read_setting_value('encCookie') == "True"
    
    with open('dataLogin/cookie.json', 'r') as f:
        data = f.read().strip()

    if is_base64_encoded(data) and not encCookie:
        decoded_data = base64.b64decode(data).decode('utf-8')
        cookies = json.loads(decoded_data)

        with open('dataLogin/cookie.json', 'w') as f:
            json.dump(cookies, f, indent=4)
        
        return cookies
    elif not is_base64_encoded(data) and encCookie:
        with open('dataLogin/cookie.json', 'r') as f:
            cookies = json.load(f)
        
        encoded_data = base64.b64encode(json.dumps(cookies).encode('utf-8')).decode('utf-8')
        
        with open('dataLogin/cookie.json', 'w') as f:
            f.write(encoded_data)
        
        return cookies
    else:
        decoded_data = base64.b64decode(data).decode('utf-8') if is_base64_encoded(data) else data
        return json.loads(decoded_data)

def read_setting_value(key):
    with open('seting.json', 'r') as f:
        settings = json.load(f)
    return settings.get(key)

def read_prefix():
    return read_setting_value('prefix')

def read_admin():
    return read_setting_value('admin')

IMEI = read_imei()
SESSION_COOKIES = read_and_format_cookies()
API_KEY = 'api_key'
SECRET_KEY = 'secret_key'
PREFIX = read_prefix()
ADMIN = read_admin()
