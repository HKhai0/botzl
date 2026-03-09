import json
import random
import os
import time
import threading

def is_json_valid(data):
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False

def fix_json_file(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Lỗi JSON: {e}. Đang tiến hành sửa...")
            file.seek(0)
            content = file.read()

            fixed_content = ''.join(c for c in content if c in '[]{},:\"\n\t 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            file.seek(0)
            file.write(fixed_content)
            file.truncate()

            print(f"File {file_path} đã được sửa.")

def monitor_json_file(file_path, interval=0.1):
    last_modified_time = os.path.getmtime(file_path)

    while True:
        current_modified_time = os.path.getmtime(file_path)
        
        if current_modified_time != last_modified_time:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if not is_json_valid(content):
                    fix_json_file(file_path)
                else:
                    pass
            
            last_modified_time = current_modified_time
        
        time.sleep(interval)

def run_load_data():
    threading.Thread(target=monitor_json_file, args=('database/database.json',), daemon=True).start()

if __name__ == "__main__":
    run_load_data()
    print("Tiến hành ghi dữ liệu data")
