import os
import requests
from config import ADMIN, PREFIX
from zlapi.models import Message
import urllib.parse
import subprocess
import json
import ast
import io
import sys

ADMIN_ID = ADMIN

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Đức Tài",
    'description': "chạy thử 1 đoạn code"
}

def is_admin(author_id):
    return author_id == ADMIN_ID
def prf():
    with open('seting.json', 'r') as f:
        return json.load(f).get('prefix')

def handle_run_command(message, message_object, thread_id, thread_type, author_id, client):
    if not is_admin(author_id):
        response_message = "• Bạn không đủ quyền hạn để sử dụng lệnh này."
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
        return
        
    command = message[len(f"{prf()}run "):]

    if command.startswith("pip uninstall"):
        command += " -y"
    
    if command.startswith(("pip", "python", "node", "npm", "sudo", "ls", "cd")):
        try:
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = result.communicate()

            if result.returncode == 0:
                response_message = stdout
            else:
                response_message = stderr
        except Exception as e:
            response_message = f"Có lỗi xảy ra: {str(e)}"
    else:
        try:
            output_buffer = io.StringIO()
            sys.stdout = output_buffer

            compiled_code = compile(command, '<string>', 'exec')
            local_vars = {}
            exec(compiled_code, {}, local_vars)

            sys.stdout = sys.__stdout__

            output = output_buffer.getvalue()
            output_buffer.close()

            if output:
                response_message = f"{output}"
            elif local_vars:
                output = "\n".join(f"{k}: {v}" for k, v in local_vars.items())
                response_message = f"{output}"
            else:
                response_message = "Done!"
                
        except SyntaxError as e:
            response_message = f"{str(e)}"
        except Exception as e:
            response_message = f"{str(e)}"
        finally:
            sys.stdout = sys.__stdout__
    
    message_to_send = Message(text=response_message)
    client.replyMessage(message_to_send, message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'run': handle_run_command
    }
