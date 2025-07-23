import time
import os
import sys
import shutil
import sqlite3
import subprocess
from utils.loaddata import run_load_data
import json
import random
from config import *
from zlapi.models import *
from zlapi.models import Message, MultiMsgStyle, MessageStyle
import threading
from mitaizl import CommandHandler
from zlapi import ZaloAPI, ZaloAPIException
from colorama import Fore, Style, init
from utils.logging_utils import Logging
from datetime import datetime
import requests
from datetime import timedelta
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from modules.noprefix.eventgroup import handle_event

temp_thread_storage = {}

uid = "270135226029167012"

init()

colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.WHITE]

text = """
██████╗ ██╗   ██╗ █████╗     ████████╗ █████╗ ██╗ 
██╔══██╗██║   ██║██╔══██     ╚══██╔══╝██╔══██╗██║
██║  ██║██║   ██║██║  ╚═╝       ██║   ███████║██║
██║  ██║██║   ██║██║  ██╗       ██║   ██╔══██║██║
██████╔╝╚██████╔╝╚█████╔╝       ██║   ██║  ██║██║
╚═════╝  ╚═════╝  ╚════╝        ╚═╝   ╚═╝  ╚═╝╚═╝
"""
for i, char in enumerate(text):
    color = colors[i % len(colors)]
    print(color + char, end='')

logger = Logging()

colors1 = [
    "FF9900", "FFFF33", "33FFFF", "FF99FF", "FF3366", "FFFF66", "FF00FF", "66FF99", "00CCFF", 
    "FF0099", "FF0066", "0033FF", "FF9999", "00FF66", "00FFFF", "CCFFFF", "8F00FF", "FF00CC", 
    "FF0000", "FF1100", "FF3300", "FF4400", "FF5500", "FF6600", "FF7700", "FF8800", "FF9900", 
    "FFaa00", "FFbb00", "FFcc00", "FFdd00", "FFee00", "FFff00", "FFFFFF", "FFEBCD", "F5F5DC", 
    "F0FFF0", "F5FFFA", "F0FFFF", "F0F8FF", "FFF5EE", "F5F5F5"
]

class ResetBot:
    def __init__(self, reset_interval=38800):
        self.reset_event = threading.Event()
        self.reset_interval = reset_interval
        self.load_autorestart_setting()

    def load_autorestart_setting(self):
        try:
            with open("seting.json", "r") as f:
                settings = json.load(f)
                self.autorestart = settings.get("autorestart", "False") == "True"
            
            if self.autorestart:
                logger.info("Chế độ auto restart đang được bật")
                threading.Thread(target=self.reset_code_periodically, daemon=True).start()
            else:
                logger.warning("Chế độ auto restart đang được tắt")
        except Exception as e:
            logger.error(f"Lỗi khi tải cấu hình autorestart: {e}")
            self.autorestart = False

    def reset_code_periodically(self):
        while not self.reset_event.is_set():
            time.sleep(self.reset_interval)
            logger.restart("Đang tiến hành khởi động lại bot...")
            self.restart_bot()

    def restart_bot(self):
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            gui_message = f"Bot khởi động lại thành công vào lúc: {current_time}"
            logger.info(gui_message)
            python = sys.executable
            os.execl(python, python, *sys.argv)
        except Exception as e:
            logger.error(f"Lỗi khi khởi động lại bot: {e}")

init(autoreset=True)

# def noti(self, event_data, event_type):
    # if event_type == GroupEventType.UNKNOWN:
        # return
    # current_time = datetime.now()
    # formatted_time = current_time.strftime("%d/%m/%Y [%H:%M:%S]")
    # thread_id = event_data['groupId']
    # group_info = self.fetchGroupInfo(thread_id)
    # if group_info and thread_id in group_info.gridInfoMap:
        # tt = group_info.gridInfoMap[thread_id]['totalMember']
    # else:
        # tt = 0
    # if event_type == GroupEventType.JOIN:
        # name_gr = event_data.groupName
        # for i, member in enumerate(event_data.updateMembers, start=0):
            # id = member['id']
            # name = member['dName']
            # count = tt + i
            # welcome_message = f"[ MITAI PROJECT NOTIFICATION GROUP ]\n> Chào mừng: {name}\n> Bạn là thành viên thứ: {count}\n> Đã tham gia nhóm: {name_gr}."

            # style = MultiMsgStyle([
            # MessageStyle(offset=0, length=len(welcome_message), style="color", color="ff6347", auto_format=False),
            # MessageStyle(offset=0, length=len(welcome_message), style="font", size="13", auto_format=False),
            # MessageStyle(offset=0, length=len(welcome_message), style="bold", auto_format=False),
            # MessageStyle(offset=39, length=len(welcome_message), style="italic", auto_format=False)
        # ])
            # styled_message = Message(text=welcome_message, style=style)

            # self.send(styled_message, thread_id, ThreadType.GROUP)

    # elif event_type == GroupEventType.LEAVE or event_type == GroupEventType.REMOVE_MEMBER:
        # name_gr = event_data.groupName
        # for i, member in enumerate(event_data.updateMembers, start=0):
            # id = member['id']
            # name = member['dName']
            # count = tt - i
            
            # if event_type == GroupEventType.REMOVE_MEMBER:
                # farewell_message = f"[ MITAI PROJECT NOTIFICATION GROUP ]\n> {name} bị xoá khỏi nhóm\n> Nhóm: {name_gr}.\n> Vào lúc: {formatted_time}\n> Tổng thành viên còn lại: {count}."
            # else:
                # farewell_message = f"[ MITAI PROJECT NOTIFICATION GROUP ]\n> {name} đã out nhóm\n> Nhóm: {name_gr}.\n> Vào lúc: {formatted_time}\n> Tổng thành viên còn lại: {count}."

            # style = MultiMsgStyle([
            # MessageStyle(offset=0, length=len(farewell_message), style="color", color="ff6347", auto_format=False),
            # MessageStyle(offset=0, length=len(farewell_message), style="font", size="13", auto_format=False),
            # MessageStyle(offset=0, length=len(farewell_message), style="bold", auto_format=False),
            # MessageStyle(offset=39, length=len(farewell_message), style="italic", auto_format=False)
        # ])
            # styled_message = Message(text=farewell_message, style=style)

            # self.send(styled_message, thread_id, ThreadType.GROUP)

def hex_to_ansi(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'\033[38;2;{r};{g};{b}m'

temp_thread_storage = {}

class Client(ZaloAPI):
    subprocess.Popen(['python', 'utils/clearCPU.py'])

    def __init__(self, api_key, secret_key, imei, session_cookies, *args, reset_interval=7200, **kwargs):
        super().__init__(api_key, secret_key, imei=imei, session_cookies=session_cookies)
        self.command_handler = CommandHandler(self)
        self.reset_bot = ResetBot(reset_interval)
        self.group_info_cache = {}
        self.last_sms_times = {}
        self.session = requests.Session()
        
        retry_strategy = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        logger.logger('EVENT GROUP', 'Tiến hành nhận sự kiện các nhóm...')

    def onLoggedIn(self, phone=None):
        self.uid = self._state.user_id
        logger.info(f"with uid: {self.uid}")
        try:
            handle_bot_admin(self)
            logger.success(f"Đã thêm 👑{get_user_name_by_id(self, self.uid)} 🆔 {self.uid} cho lần đầu tiên khởi động vào danh sách ADMIN_BOT ✅")
        except Exception as e:
            logger.error(f"{str(e)}")

    def onEvent(self, event_data, event_type):
        # noti(self, event_data, event_type)
        handle_event(self, event_data, event_type)
        thread = threading.Thread(target=self.handle_event, args=(event_data, event_type))
        thread.daemon = True
        thread.start()

    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):

        if isinstance(message, str):
                self.command_handler.handle_command(message, author_id, message_object, thread_id, thread_type)
                
        try:
            message_text = message.text if isinstance(message, Message) else str(message)
            author_info = self.fetchUserInfo(author_id).changed_profiles.get(author_id, {})
            author_name = author_info.get('zaloName', 'Không xác định')

            group_info = self.fetchGroupInfo(thread_id)
            group_name = group_info.gridInfoMap.get(thread_id, {}).get('name', 'None')

            current_time = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime())

            colors_selected = random.sample(colors1, 9)
            output = (
                f"{hex_to_ansi(colors_selected[0])}{Style.BRIGHT}------------------------------{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[1])}{Style.BRIGHT}• Message: {message_text}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[1])}{Style.BRIGHT}• Message ID: {mid}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[2])}{Style.BRIGHT}• ID NGƯỜI DÙNG: {author_id}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[6])}{Style.BRIGHT}• TÊN NGƯỜI DÙNG: {author_name}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[3])}{Style.BRIGHT}• ID NHÓM: {thread_id}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[4])}{Style.BRIGHT}• TÊN NHÓM: {group_name}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[5])}{Style.BRIGHT}• TYPE: {thread_type}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[7])}{Style.BRIGHT}• THỜI GIAN NHẬN ĐƯỢC: {current_time}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[0])}{Style.BRIGHT}------------------------------{Style.RESET_ALL}"
            )
            print(output)

            if author_id == uid:
                return

            if thread_type == ThreadType.USER:
                now = time.time()
                if author_id in temp_thread_storage:
                    last_message_time = temp_thread_storage[author_id]
                    if now - last_message_time < 7200:
                        return
                msg = f"crkd"
                styles = MultiMsgStyle([
            MessageStyle(offset=0, length=2, style="color", color="#a24ffb", auto_format=False),
            MessageStyle(offset=2, length=len(msg) - 2, style="color", color="#ffaf00", auto_format=False),
            MessageStyle(offset=0, length=40, style="color", color="#a24ffb", auto_format=False),
            MessageStyle(offset=45, length=len(msg) - 2, style="color", color="#ffaf00", auto_format=False),
            MessageStyle(offset=0, length=len(msg), style="font", size="3", auto_format=False),
            MessageStyle(offset=0, length=len(msg), style="bold", auto_format=False),
            MessageStyle(offset=0, length=len(msg), style="italic", auto_format=False)
        ])
                self.replyMessage(Message(text=msg, style=styles),message_object, thread_id, thread_type)
                temp_thread_storage[author_id] = now

        except Exception as e:
            logger.error(f"Lỗi xử lý tin nhắn: {e}")

if __name__ == "__main__":
    try:
        client = Client(API_KEY, SECRET_KEY, IMEI, SESSION_COOKIES)
        client.listen(thread=True, delay=0)
    except Exception as e:
        logger.error(f"Lỗi rồi, Không thể đăng nhập...: {str(e)}")
        # python = sys.executable
        # os.execl(python, python, *sys.argv)
        # time.sleep(10)
