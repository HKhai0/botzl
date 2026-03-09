import re
import os
import requests
from zlapi.models import Message
from bs4 import BeautifulSoup
import json
import ffmpeg

des = {
    'version': "1.0.8",
    'credits': "Nguyễn Đức Tài",
    'description': "Tải video hoặc ảnh từ link (capcut, tiktok, youtube, facebook, douyin, pinterest, ig,...)"
}

def key():
    with open('seting.json', 'r') as f:
        return json.load(f).get('key')

def handle_down_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip()
    video_link = message_object.href if message_object.href else None

    def extract_links(content):
        urls = re.findall(r'(https?://[^\s]+)', content)
        soup = BeautifulSoup(content, "html.parser")
        href_links = [a['href'] for a in soup.find_all('a', href=True)]
        return urls + href_links

    if not video_link:
        links = extract_links(content)
        if not links:
            error_message = Message(text="Vui lòng nhập một đường link cần down hợp lệ.")
            client.replyMessage(error_message, message_object, thread_id, thread_type)
            return
        video_link = links[0].strip()

    def downall(video_link):
        try:
            api_url = f'https://api.hungdev.id.vn/media/downAIO?url={video_link}&apikey={key()}'
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            
            if data.get('success') and data.get('data'):
                medias = data['data'].get('medias', [])
                tit = data['data'].get('title', 'Không có tiêu đề')
                dang = data['data'].get('source', 'Không có nguồn')

                image_links = []
                video_url = None

                for media in medias:
                    media_type = media.get('type')
                    if media_type == 'image':
                        image_links.append(media.get('url'))
                    elif media_type == 'video':
                        quality = media.get('quality')
                        desired_qualities = ['360p', 'no_watermark', 'SD', 'No Watermark', 'Full HD']
                        if quality in desired_qualities:
                            video_url = media.get('url')

                return image_links, video_url, tit, dang

        except requests.exceptions.RequestException as e:
            raise Exception(f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        except KeyError as e:
            raise Exception(f"Dữ liệu từ API không đúng cấu trúc: {str(e)}")
        except Exception as e:
            raise Exception(f"Đã xảy ra lỗi không xác định: {str(e)}")

    try:
        image_urls, video_url, tit, dang = downall(video_link)
        sendtitle = f"Thể loại: {dang}\nTiêu đề: {tit}"
        headers = {'User-Agent': 'Mozilla/5.0'}

        if image_urls:
            image_paths = []
            for index, image_url in enumerate(image_urls):
                image_response = requests.get(image_url, headers=headers)
                image_path = f'modules/cache/{index + 1}.jpeg'
                
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)

                image_paths.append(image_path)

            if all(os.path.exists(image_path) for image_path in image_paths):
                message_to_send = Message(text=sendtitle)
                client.sendMultiLocalImage(
                    imagePathList=image_paths, 
                    message=message_to_send,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    width=1200,
                    height=1600
                )
                for image_path in image_paths:
                    os.remove(image_path)
            else:
                raise Exception("Không có ảnh")

        elif video_url:
            messagesend = Message(text=sendtitle)
            thumbnailUrl = 'https://f59-zpg-r.zdn.vn/jpg/3574552058519415218/d156abc8a66e1f30467f.jpg'
            duration = '99999999999999999999'

            client.sendRemoteVideo(
                video_url, 
                thumbnailUrl,
                duration=duration,
                message=messagesend,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1200,
                height=1600
            )

        else:
            error_message = Message(text="Không tìm thấy video hoặc ảnh với yêu cầu.")
            client.sendMessage(error_message, thread_id, thread_type)
    
    except Exception as e:
        error_message = Message(text=str(e))
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'down': handle_down_command
    }
