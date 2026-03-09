from zlapi.models import Message
import requests

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Tải file nhạc từ link soundcloud"
}

def get_file_size(url):
    try:
        response = requests.head(url)
        size = response.headers.get('Content-Length', None)
        if size:
            return int(size)
        return None
    except requests.RequestException:
        return None

def handle_sound_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 2:
        error_message = Message(text="Vui lòng nhập một đường link SoundCloud hợp lệ.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    linksound = content[1].strip()

    if not linksound.startswith("https://"):
        error_message = Message(text="Vui lòng nhập một đường link SoundCloud hợp lệ.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    try:
        apikey = f'http://www.hungdev.id.vn/getApiKey'
        res = requests.get(apikey)
        res.raise_for_status()

        data = res.json()

        key = data['data'].get('key')

        api_url = f'http://www.hungdev.id.vn/media/downAIO?apikey={key}&url={linksound}&model=v1'
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        if not data.get('success', False):
            raise KeyError("API trả về kết quả không thành công.")

        medias = data['data'].get('medias', [])

        if isinstance(medias, list) and len(medias) > 0:
            media = medias[0]
            voiceUrl = media.get('url')
            extension = media.get('extension', 'mp3')
            duration = data['data'].get('duration', "0:00")
        else:
            raise KeyError("Không tìm thấy URL trong dữ liệu API.")

        titlesound = data['data'].get('title', 'Không có tiêu đề')
        sendtitle = f"Tiêu đề: {titlesound}.{extension} (Thời lượng: {duration})\nBot đang tiến hành gửi file nhạc vui lòng chờ :3 :3 :3"
        
        messagesend = Message(text=sendtitle)
        client.replyMessage(messagesend, message_object, thread_id, thread_type)

        fileSize = get_file_size(voiceUrl)
        if fileSize is None:
            fileSize = 5000000

        file_name = f"{titlesound}.{extension}" if not titlesound.endswith('.mp3') else titlesound

        client.sendRemoteFile(
            fileUrl=voiceUrl,
            thread_id=thread_id,
            thread_type=thread_type,
            fileName=file_name,
            fileSize=None,
            extension=extension
        )

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except KeyError as e:
        error_message = Message(text=f"Dữ liệu từ API không đúng cấu trúc: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi không xác định: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'sound': handle_sound_command
    }
