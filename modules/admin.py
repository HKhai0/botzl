import json
from zlapi.models import Message
from config import ADMIN

des = {
    'version': "1.0.6",
    'credits': "Nguyễn Đức Tài",
    'description': "Quản lý danh sách admin"
}

def is_admin(author_id):
    return author_id == ADMIN

def add_admin(uid, name):
    with open('seting.json', 'r') as f:
        data = json.load(f)

    if uid in data['adm']:
        return f"• {name} đã có admin trước đó."

    data['adm'].append(uid)

    with open('seting.json', 'w') as f:
        json.dump(data, f, indent=4)

    return f"• Đã thêm người dùng {name} vào danh sách admin bot"

def remove_admin(uid, name):
    with open('seting.json', 'r') as f:
        data = json.load(f)

    if uid not in data['adm']:
        return f"• {name} chưa có ở danh sách admin."

    data['adm'].remove(uid)

    with open('seting.json', 'w') as f:
        json.dump(data, f, indent=4)

    return f"• Đã xoá {name} khỏi danh sách admin bot"

def list_admins(client):
    with open('seting.json', 'r') as f:
        data = json.load(f)
        
    admins_list = data.get('adm', [])
    if not admins_list:
        return "• Danh sách admin bot trống."

    admin_text = "[ DANH SÁCH ADMIN BOT MITAIZL ]\n\n"
    for idx, uid in enumerate(admins_list, 1):
        author_info = client.fetchUserInfo(uid).changed_profiles.get(uid, {})
        author_name = author_info.get('zaloName', 'Không xác định')
        admin_text += f"{idx}:\n• Name: {author_name}\n• ID: {uid}\n\n"
    return admin_text

def handle_admin_command(message, message_object, thread_id, thread_type, author_id, client):
    if not is_admin(author_id):
        response_message = "• Bạn không đủ quyền hạn để sử dụng lệnh này."
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
        return

    text = message.split()
    if len(text) < 2:
        error_message = Message(text="• Vui lòng nhập lệnh hợp lệ.\n• add <@tag>\n• remove <@tag>\n• list")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    subcommand = text[1].lower()
    if subcommand == "add" and len(message_object.mentions) > 0:
        uid = message_object.mentions[0]['uid']
        author_info = client.fetchUserInfo(uid).changed_profiles.get(uid, {})
        name = author_info.get('zaloName', 'Không xác định')
        response_message = add_admin(uid, name)

    elif subcommand == "remove" and len(message_object.mentions) > 0:
        uid = message_object.mentions[0]['uid']
        author_info = client.fetchUserInfo(uid).changed_profiles.get(uid, {})
        name = author_info.get('zaloName', 'Không xác định')
        response_message = remove_admin(uid, name)

    elif subcommand == "list":
        response_message = list_admins(client)

    else:
        response_message = "• Lệnh không hợp lệ. Vui lòng sử dụng: admin add <@tag>, admin remove <@tag> hoặc adm list."

    message_to_send = Message(text=response_message)
    client.replyMessage(message_to_send, message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'admin': handle_admin_command
    }
