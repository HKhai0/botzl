import json
from zlapi.models import Message, ThreadType
from config import ADMIN

des = {
    'version': "3.6.7",
    'credits': "Lê Hữu Khải (Python Is Trash)",
    'description': "AI config",
}

def is_admin(author_id):
    return author_id == ADMIN

def load_status():
    """Return the entire AI configuration file as a dict.

    The file is expected to contain at least the following keys:
    ``threads`` (a list of thread IDs where the feature is enabled) and
    ``mode`` (a string indicating the current mode).
    """
    try:
        with open("aicfg.json", "r") as f:
            return json.load(f)
    except Exception:
        # missing or invalid config -> fallback to defaults
        return {"threads": [], "mode": "default"}

def save_status(data):
    """Persist the entire configuration dict to disk."""
    with open("aicfg.json", "w") as f:
        json.dump(data, f, indent=4)

def handle_ai_command(message, message_object, thread_id, thread_type, author_id, client):
    if not is_admin(author_id):
        response_message = "Bạn không có quyền sử dụng lệnh này."
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
        return
    else:
        input_value1 = message.split()[1].lower() if len(message.split()) > 1 else None
        input_value2 = message.split()[2].lower() if len(message.split()) > 2 else None
        input_value3 = message.split()[3].lower() if len(message.split()) > 3 else None
        input_value4 = message.split()[4].lower() if len(message.split()) > 4 else None
    
    
        cfg = load_status()
        threads = cfg.get("threads", [])
        mode = cfg.get("mode", "default")
    
    
        if input_value1 == "set": #eg : ai set {option}
        
            if input_value2 == "enable":
            
                if thread_id not in threads:
                    threads.append(thread_id)
                    cfg["threads"] = threads
                    save_status(cfg)
                    response_message = "Đã bật tính năng AI cho nhóm này."
                else:
                    response_message = "Tính năng AI đã được bật cho nhóm này."
            elif input_value2 == "disable":
                if thread_id in threads:
                    threads.remove(thread_id)
                    cfg["threads"] = threads
                    save_status(cfg)
                    response_message = "Đã tắt tính năng AI cho nhóm này."
                else:
                    response_message = "Tính năng AI đã được tắt cho nhóm này."
            else:
                response_message = "Cú pháp không đầy đủ , vui lòng dùng ai để biết thêm"
        elif input_value1 == "get":
        
            if input_value2 == "status":
                if thread_id in threads:
                    response_message = "Tính năng AI đang được bật cho nhóm này."
                else:
                    response_message = "Tính năng AI đang được tắt cho nhóm này."
            elif input_value2 == "threads":
                if threads:
                    response_message = "Các nhóm đã bật tính năng AI:\n" + "\n".join(f"- {tid}" for tid in threads)
                else:
                    response_message = "Chưa có nhóm nào bật tính năng AI."
            elif input_value2 == "mode":
                response_message = f"Chế độ hiện tại là '{mode}'."
            
            else:
                response_message = "Cú pháp không đầy đủ , vui lòng dùng ai để biết thêm"
        elif input_value1 == "mode":
            
            if input_value2 == "admin":
                mode = "admin"
                cfg["mode"] = mode
                save_status(cfg)
                response_message = "Đã chuyển sang chế độ admin. Chỉ admin mới có thể sử dụng tính năng AI."
            elif input_value2 == "all":
                mode = "all"
                cfg["mode"] = mode
                save_status(cfg)
                response_message = "Đã chuyển sang chế độ all. Tất cả thành viên đều có thể sử dụng tính năng AI."
            elif input_value2 == "community":
                mode = "community"
                cfg["mode"] = mode
                save_status(cfg)
                response_message = "Đã chuyển sang chế độ community. AI sẽ kích hoạt với mọi đối tượng trừ blacklist trong group này"
            elif input_value2 == "default":
                mode = "default"
                cfg["mode"] = mode
                save_status(cfg)
                response_message = "Đã chuyển về chế độ mặc định. AI sẽ kích hoạt theo điều kiện của trigger đã cài đặt"
            else:
                response_message = "Cú pháp không đầy đủ , vui lòng dùng ai để biết thêm"
        elif input_value1 == "trigger":
            if input_value2 == "show":
                triggers = cfg.get("triggers", [])
                if triggers:
                    response_message = "Các trigger đã cài đặt:\n" + "\n".join(f"- {t}" for t in triggers)
                else:
                    response_message = "Chưa có trigger nào được cài đặt."
            else:
                response_message = "Cú pháp không đầy đủ , vui lòng dùng ai để biết thêm"
        elif input_value1 == "aiprefix":
            if input_value2 == "show":
                aiprefix = cfg.get("aiprefix", "Không có aiprefix nào được cài đặt.")
                response_message = f"Prefix hiện tại là: {aiprefix}"
            elif input_value2 == "set":
                if input_value3:
                    cfg["aiprefix"] = input_value3
                    save_status(cfg)
                    response_message = f"Đã đặt aiprefix mới: {input_value3}"
                else:
                    response_message = "Cú pháp không đầy đủ , vui lòng dùng ai để biết thêm"
            else:
                response_message = "Cú pháp không đầy đủ , vui lòng dùng ai để biết thêm"
    
    
    
        
    
    
        else: #this is the help section
            response_message = "Hướng dẫn sử dụng lệnh ai:\n"
    
    
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
    
def get_mitaizl():
    return {
        'ai': handle_ai_command
    }