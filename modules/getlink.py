from zlapi.models import Message
import json
import urllib.parse

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Đức Tài x TRBAYK",
    'description': "Getlink hình ảnh, file, gif, link, video"
}

last_sent_image_url = None  

def handle_getlink_command(message, message_object, thread_id, thread_type, author_id, client):
    global last_sent_image_url
    msg_obj = message_object

    if msg_obj.msgType == "chat.photo":
        img_url = msg_obj.content.href.replace("\\/", "/")
        img_url = urllib.parse.unquote(img_url)
        last_sent_image_url = img_url
        send_image_link(img_url, thread_id, thread_type, client)

    elif msg_obj.quote:
        attach = msg_obj.quote.attach
        if attach:
            try:
                attach_data = json.loads(attach)
            except json.JSONDecodeError as e:
                print(f"Lỗi khi phân tích JSON: {str(e)}")
                return

            image_url = attach_data.get('hdUrl') or attach_data.get('href')
            if image_url:
                send_image_link(image_url, thread_id, thread_type, client)
            else:
                send_error_message(thread_id, thread_type, client)
        else:
            send_error_message(thread_id, thread_type, client)
    else:
        send_error_message(thread_id, thread_type, client)

def send_image_link(image_url, thread_id, thread_type, client):
    if image_url:
        message_to_send = Message(text=f"{image_url}")
        
        if hasattr(client, 'send'):
            client.send(message_to_send, thread_id, thread_type)
        else:
            print("Client không hỗ trợ gửi tin nhắn.")

def send_error_message(thread_id, thread_type, client):
    error_message = Message(text="Vui lòng reply(phản hồi) hình ảnh, gif, file, video cần getlink.")
    
    if hasattr(client, 'send'):
        client.send(error_message, thread_id, thread_type)
    else:
        print("Client không hỗ trợ gửi tin nhắn.")

def get_mitaizl():
    return {
        'getlink': handle_getlink_command
    }
