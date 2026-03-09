import os
import random
from zlapi.models import Message, MultiMsgStyle, MessageStyle
import importlib

colors = [
    "FF9900", "FFFF33", "33FFFF", "FF99FF", "FF3366", "FFFF66", "FF00FF", "66FF99", "00CCFF", 
    "FF0099", "FF0066", "0033FF", "FF9999", "00FF66", "00FFFF", "CCFFFF", "8F00FF", "FF00CC", 
    "FF0000", "FF1100", "FF3300", "FF4400", "FF5500", "FF6600", "FF7700", "FF8800", "FF9900", 
    "FFaa00", "FFbb00", "FFcc00", "FFdd00", "FFee00", "FFff00", "FFFFFF", "FFEBCD", "F5F5DC", 
    "F0FFF0", "F5FFFA", "F0FFFF", "F0F8FF", "FFF5EE", "F5F5F5"
]

so = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Xem toàn bộ lệnh hiện có của bot"
}

def get_all_mitaizl():
    mitaizl = {}

    for module_name in os.listdir('modules'):
        if module_name.endswith('.py') and module_name != '__init__.py':
            module_path = f'modules.{module_name[:-3]}'
            module = importlib.import_module(module_path)

            if hasattr(module, 'get_mitaizl'):
                module_mitaizl = module.get_mitaizl()
                mitaizl.update(module_mitaizl)

    command_names = list(mitaizl.keys())
    return command_names

def handle_menu_command(message, message_object, thread_id, thread_type, author_id, client):
    command_names = get_all_mitaizl()

    total_mitaizl = len(command_names)
    numbered_mitaizl = [f"{i+1}. {name}" for i, name in enumerate(command_names)]
    menu_message = f"Tổng số lệnh bot hiện tại có: {total_mitaizl} lệnh \nDưới đây là các lệnh hiện có của bot:\n" + "\n".join(numbered_mitaizl)

    msg_length = len(menu_message)
    random_color = random.choice(colors)
    random_so = random.choice(so)

    style = MultiMsgStyle([
        MessageStyle(offset=0, length=msg_length, style="color", color=random_color, auto_format=False),
        MessageStyle(offset=0, length=msg_length, style="size", size=random_so, auto_format=True),
        MessageStyle(offset=0, length=msg_length, style="bold", auto_format=False)
    ])

    message_to_send = Message(text=menu_message, style=style)
    client.replyMessage(message_to_send, message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'menu': handle_menu_command
    }
