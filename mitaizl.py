import os
import importlib
import sys
import subprocess
import random
import time
import json
import datetime
import pytz
import threading
from zlapi._message import Mention
from zlapi.models import Message
from zlapi.models import *
from collections import defaultdict
from config import PREFIX, ADMIN
from utils.logging_utils import Logging
from colorama import Fore

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules/auto'))

logger = Logging()

def prf():
    with open('seting.json', 'r') as f:
        return json.load(f).get('prefix')

def adm():
    with open('seting.json', 'r') as f:
        return json.load(f).get('adm')

def load_duyetbox_data():
    try:
        with open('modules/cache/duyetboxdata.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

class CommandHandler:
    def __init__(self, client):
        self.client = client
        self.mitaizl = self.load_mitaizl()
        self.noprefix_mitaizl = self.load_noprefix_mitaizl()
        self.auto_mitaizl = self.load_auto_mitaizl()
        self.admin_id = ADMIN
        self.adminon = self.load_admin_mode()
        self.command_usage = {}

        if PREFIX == '':
            logger.prefixcmd("Prefix hiện tại của bot là 'no prefix'")
        else:
            logger.prefixcmd(f"Prefix hiện tại của bot là '{PREFIX}'")

    def load_admin_mode(self):
        with open('modules/cache/admindata.json', 'r') as f:
            return json.load(f).get('adminon')

    def save_admin_mode(self):
        with open('modules/cache/admindata.json', 'w') as f:
            json.dump({'adminon': self.adminon}, f)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb_color):
        return '{:02x}{:02x}{:02x}'.format(*rgb_color)

    def generate_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def generate_gradient_colors(self, length, num_colors=5):
        random_colors = [self.generate_random_color() for _ in range(num_colors)]
        rgb_colors = [self.hex_to_rgb(color) for color in random_colors]

        colors = []
        for j in range(num_colors - 1):
            start_rgb = rgb_colors[j]
            end_rgb = rgb_colors[j + 1]
            segment_length = length // (num_colors - 1)
            
            for i in range(segment_length):
                interpolated_color = (
                    int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / (segment_length - 1)),
                    int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / (segment_length - 1)),
                    int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / (segment_length - 1))
                )
                colors.append(self.rgb_to_hex(interpolated_color))
        
        return colors

    def create_rainbow_params(self, text, size=20):
        styles = []
        colors = self.generate_gradient_colors(len(text), num_colors=5)
        
        for i, color in enumerate(colors):
            styles.append({"start": i, "len": 1, "st": f"c_{color}"})
        
        params = {"styles": styles, "ver": 0}
        return json.dumps(params)

    def sendMessageColor(self, error_message, thread_id, thread_type):
        stype = self.create_rainbow_params(error_message)
        mes = Message(
            text=error_message,
            style=stype
        )
        self.client.send(mes, thread_id, thread_type)

    def replyMessageColor(self, error_message, message_object, thread_id, thread_type):
        stype = self.create_rainbow_params(error_message)
        mes = Message(
            text=error_message,
            style=stype
        )
        self.client.replyMessage(mes, message_object, thread_id=thread_id, thread_type=thread_type, ttl=5000)

    def load_mitaizl(self):
        mitaizl = {}
        modules_path = 'modules'
        success_count = 0
        failed_count = 0
        success_mitaizl = []
        failed_mitaizl = []

        for filename in os.listdir(modules_path):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f'{modules_path}.{module_name}')
                    
                    if hasattr(module, 'get_mitaizl'):
                        if hasattr(module, 'des'):
                            des = getattr(module, 'des')
                            if all(key in des for key in ['version', 'credits', 'description']):
                                mitaizl.update(module.get_mitaizl())
                                success_count += 1
                                success_mitaizl.append(module_name)
                            else:
                                raise ImportError(f"Lỗi không thể tìm thấy thông tin của lệnh: {module_name}")
                        else:
                            raise ImportError(f"Lệnh {module_name} không có thông tin")
                    else:
                        raise ImportError(f"Module {module_name} không có hàm gọi lệnh")
                except Exception as e:
                    logger.error(f"Không thể load được module: {module_name}. Lỗi: {e}")
                    failed_count += 1
                    failed_mitaizl.append(module_name)

        if success_count > 0:
            logger.success(f"Đã load thành công {success_count} lệnh")
        if failed_count > 0:
            logger.warning(f"Không thể load được {failed_count} lệnh: {', '.join(failed_mitaizl)}")

        return mitaizl

    def load_noprefix_mitaizl(self):
        noprefix_mitaizl = {}
        noprefix_modules_path = 'modules.noprefix'
        success_count = 0
        failed_count = 0
        success_noprefix_mitaizl = []
        failed_noprefix_mitaizl = []

        for filename in os.listdir('modules/noprefix'):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f'{noprefix_modules_path}.{module_name}')
                    
                    if hasattr(module, 'get_mitaizl'):
                        if hasattr(module, 'des'):
                            des = getattr(module, 'des')
                            if all(key in des for key in ['version', 'credits', 'description']):
                                noprefix_mitaizl.update(module.get_mitaizl())
                                success_count += 1
                                success_noprefix_mitaizl.append(module_name)
                            else:
                                raise ImportError(f"Module {module_name} thiếu các thông tin cần thiết")
                        else:
                            raise ImportError(f"Lệnh {module_name} không có thông tin")
                    else:
                        raise ImportError(f"Module {module_name} không có hàm gọi lệnh")
                except Exception as e:
                    logger.error(f"Không thể load được module: {module_name}. Lỗi: {e}")
                    failed_count += 1
                    failed_noprefix_mitaizl.append(module_name)

        if success_count > 0:
            logger.success(f"Đã load thành công {success_count} lệnh noprefix")
        if failed_count > 0:
            logger.warning(f"Không thể load được {failed_count} lệnh noprefix: {', '.join(failed_noprefix_mitaizl)}")

        return noprefix_mitaizl

    def load_auto_mitaizl(self):
        auto_mitaizl = {}
        auto_modules_path = 'modules/auto'
        success_count = 0
        failed_count = 0
        success_auto_mitaizl = []
        failed_auto_mitaizl = []

        for filename in os.listdir(auto_modules_path):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f'modules.auto.{module_name}')
                    
                    if hasattr(module, 'start_auto'):
                        auto_mitaizl[module_name] = module
                        success_count += 1
                        success_auto_mitaizl.append(module_name)
                    else:
                        raise ImportError(f"Module {module_name} không có hàm start_auto")
                except Exception as e:
                    logger.error(f"Không thể load module auto: {module_name}. Lỗi: {e}")
                    failed_count += 1
                    failed_auto_mitaizl.append(module_name)

        if success_count > 0:
            logger.success(f"Đã load thành công {success_count} lệnh auto")
            for module in success_auto_mitaizl:
                threading.Thread(target=auto_mitaizl[module].start_auto, args=(self.client,)).start()
        if failed_count > 0:
            logger.warning(f"Không thể load {failed_count} lệnh auto: {', '.join(failed_auto_mitaizl)}")

        return auto_mitaizl

    def toggle_admin_mode(self, message, message_object, thread_id, thread_type, author_id):
        if author_id == self.admin_id:
            if 'on' in message.lower():
                self.adminon = True
                self.save_admin_mode()
                self.replyMessageColor("Chế độ admin đã được bật.", message_object, thread_id, thread_type)
            elif 'off' in message.lower():
                self.adminon = False
                self.save_admin_mode()
                self.replyMessageColor("Chế độ admin đã được tắt.", message_object, thread_id, thread_type)
            else:
                self.replyMessageColor("Vui lòng sử dụng lệnh: adminmode on/off.", message_object, thread_id, thread_type)
        else:
            self.replyMessageColor("Bạn không có quyền bật/tắt chế độ admin.", message_object, thread_id, thread_type)

    def handle_command(self, message, author_id, message_object, thread_id, thread_type):
        current_time = time.time()
        if author_id not in self.command_usage:
            self.command_usage[author_id] = []

        self.command_usage[author_id] = [t for t in self.command_usage[author_id] if current_time - t < 2]

        if len(self.command_usage[author_id]) >= 4:
            def delayed_reaction():
                icon = "⏳"
                self.client.sendReaction(
                    messageObject=message_object, 
                    reactionIcon=icon, 
                    thread_id=thread_id, 
                    thread_type=thread_type
                )

            threading.Thread(target=delayed_reaction).start()
            return

        self.command_usage[author_id].append(current_time)

        if message.startswith(prf()) and thread_id not in load_duyetbox_data() and author_id not in adm():
            gui = Message(text="> Nhóm của bạn chưa được duyệt!\n> Để dùng được bot vui lòng liên hệ đến Admin Nguyễn Đức Tài để được duyệt và dùng bot.\nLink facebook: https://www.facebook.com/duck.tai206\n> Zalo: 0766314906")
            self.client.replyMessage(gui, message_object, thread_id, thread_type, ttl=120000)
            return

        if message.startswith(prf() + 'adminmode'):
            self.toggle_admin_mode(message, message_object, thread_id, thread_type, author_id)
            return

        noprefix_command_handler = self.noprefix_mitaizl.get(message.lower())
        if noprefix_command_handler:
            noprefix_command_handler(message, message_object, thread_id, thread_type, author_id, self.client)
            return

        if not message.startswith(prf()):
            return

        command_name = message[len(prf()):].split(' ')[0].lower()
        command_handler = self.mitaizl.get(command_name)

        if self.adminon and author_id not in adm():
            error_message = "Chế độ admin đang bật, chỉ có admin mới có thể sử dụng lệnh."
            self.replyMessageColor(error_message, message_object, thread_id, thread_type)
            return

        if command_handler:
            command_handler(message, message_object, thread_id, thread_type, author_id, self.client)
        else:
            error_message = Message(text=f"Không tìm thấy lệnh: '{command_name}'. Hãy dùng {prf()}menu để biết các lệnh có trên hệ thống.")
            self.client.replyMessage(error_message, message_object, thread_id, thread_type, ttl=20000)
