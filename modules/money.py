import json
import random
import time
import os
from zlapi.models import Message
from config import ADMIN

des = {
    'version': "1.0.6",
    'credits': "Nguyễn Đức Tài",
    'description': "Quản lý tiền trong bot"
}

user_cooldowns = {}

def is_admin(author_id):
    return author_id == ADMIN

def load_money_data():
    try:
        with open('modules/cache/money.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_money_data(data):
    with open('modules/cache/money.json', 'w') as f:
        json.dump(data, f, indent=4)

def format_money(amount):
    return f"{amount:,} VNĐ"

def get_user_name(client, user_id):
    try:
        user_info = client.fetchUserInfo(user_id)
        profile = user_info.changed_profiles.get(user_id, {})
        return profile.get('zaloName', 'Không xác định')
    except AttributeError:
        return 'Không xác định'

def handle_money_command(message, message_object, thread_id, thread_type, author_id, client):
    text = message.split()
    money_data = load_money_data()
    
    if len(text) < 2:
        response_message = "Vui lòng dùng\n• money pay <số tiền> <@tag>\n• money check (check số tiền bản thân hoặc người được tag)\n• money top (check 10 người có số tiền cao nhất)\n• money daily (nhận ngẫu nhiên số tiền free)"
        client.replyMessage(Message(text=response_message), message_object, thread_id, thread_type)
        return

    response_message = ""

    if text[1] == "set" and is_admin(author_id):
        if len(text) < 3 or not text[2].isdigit() or len(message_object.mentions) < 1:
            response_message = "• Vui lòng nhập số hợp lệ và tag người nhận."
        else:
            amount = int(text[2])
            target_id = message_object.mentions[0]['uid']
            target_name = get_user_name(client, target_id)
            money_data[target_id] = money_data.get(target_id, 0) + amount
            save_money_data(money_data)
            response_message = f"• Đã cộng {format_money(amount)} cho {target_name}."

    elif text[1] == "add" and is_admin(author_id):
        if len(text) < 3 or not text[2].isdigit():
            response_message = "• Vui lòng nhập số hợp lệ."
        else:
            amount = int(text[2])
            money_data[author_id] = money_data.get(author_id, 0) + amount
            save_money_data(money_data)
            response_message = f"• Đã tự động cộng thêm {format_money(amount)} cho bản thân."

    elif text[1] == "reset" and is_admin(author_id):
        os.remove('modules/cache/money.json')
        response_message = "Reset lại thành công toàn bộ số dư hệ thống"

    elif text[1] == "remove" and is_admin(author_id):
        if len(text) < 3:
            response_message = "• Vui lòng chỉ định số tiền hoặc 'all'."
        else:
            target_id = message_object.mentions[0]['uid'] if len(message_object.mentions) > 0 else author_id
            target_name = get_user_name(client, target_id)

            if text[2] == "all":
                money_data[target_id] = 0
                response_message = f"• Đã trừ thành công toàn bộ tiền của {target_name}."
            elif text[2].isdigit():
                amount = int(text[2])
                money_data[target_id] = max(0, money_data.get(target_id, 0) - amount)
                response_message = f"• Đã trừ {format_money(amount)} của {target_name}."
            else:
                response_message = "• Vui lòng nhập số hợp lệ."

            save_money_data(money_data)

    elif text[1] == "daily":
        current_time = time.time()
        cooldown_time = 180

        if author_id in user_cooldowns:
            time_since_last_use = current_time - user_cooldowns[author_id]
            if time_since_last_use < cooldown_time:
                remaining_time = cooldown_time - time_since_last_use
                error_message = Message(text=f"Bạn phải đợi {int(remaining_time // 60)} phút {int(remaining_time % 60)} giây nữa mới có thể nhận tiền free.")
                client.replyMessage(error_message, message_object, thread_id, thread_type)
                return

        amount = random.randint(10000, 500000)
        money_data[author_id] = money_data.get(author_id, 0) + amount
        user_cooldowns[author_id] = current_time
        save_money_data(money_data)
        response_message = f"• Bạn đã nhận được ngẫu nhiên {format_money(amount)}."

    elif text[1] == "pay":
        if len(text) < 3 or not text[2].isdigit() or len(message_object.mentions) < 1:
            response_message = "• Vui lòng nhập số hợp lệ và tag người nhận."
        else:
            amount = int(text[2])
            target_id = message_object.mentions[0]['uid']
            target_name = get_user_name(client, target_id)

            if money_data.get(author_id, 0) >= amount:
                money_data[author_id] -= amount
                money_data[target_id] = money_data.get(target_id, 0) + amount
                save_money_data(money_data)
                response_message = f"• Chuyển thành công {format_money(amount)} đến {target_name}."
            else:
                response_message = "• Số dư không đủ để thực hiện giao dịch."

    elif text[1] == "top":
        top_users = sorted(money_data.items(), key=lambda x: x[1], reverse=True)[:10]
        response_message = "[ TOP NGƯỜI CÓ SỐ TIỀN CAO NHẤT ]\n"
        for idx, (uid, amount) in enumerate(top_users, 1):
            name = get_user_name(client, uid)
            response_message += f"• Top {idx}:\n> Name: {name}\n> Số tiền: {format_money(amount)}\n\n"

    elif text[1] == "check":
        if message_object.mentions:
            target_id = message_object.mentions[0]['uid']
            target_name = get_user_name(client, target_id)
            balance = money_data.get(target_id, 0)
            response_message = f"• {target_name} hiện có: {format_money(balance)}."
        else:
            balance = money_data.get(author_id, 0)
            response_message = f"• Số tiền của bạn hiện có: {format_money(balance)}."

    else:
        response_message = "• Lệnh không hợp lệ hoặc bạn không có quyền sử dụng lệnh này."

    client.replyMessage(Message(text=response_message), message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'money': handle_money_command
    }
    