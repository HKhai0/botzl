import requests
import os
from datetime import datetime
from zlapi.models import Message, ZaloAPIException
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "info người dùng(tag)"
}

def create_canvas(user_data):
    background_image = Image.open("nen.jpeg")
    draw = ImageDraw.Draw(background_image)

    bg_width, bg_height = background_image.size

    avatar_url = user_data.get('avatar')
    avatar_image = None
    if avatar_url:
        response = requests.get(avatar_url)
        avatar_image = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        avatar_image = Image.open("default_avatar.jpg").convert("RGB")

    avatar_size = (550, 550)
    avatar_image = ImageOps.fit(avatar_image, avatar_size, centering=(0.5, 0.5))

    mask = Image.new("L", avatar_size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0) + avatar_size, fill=255)

    avatar_image.putalpha(mask)

    avatar_x = bg_width - avatar_size[0] - 30
    avatar_y = (bg_height - avatar_size[1]) // 2

    background_image.paste(avatar_image, (avatar_x, avatar_y), avatar_image)

    fontc = "modules/cache/UTM-AvoBold.ttf"

    font_title = ImageFont.truetype(fontc, 45)
    font_info = ImageFont.truetype(fontc, 35)
    font_bio = ImageFont.truetype(fontc, 30)

    draw.text((100, 100), "Tên:", font=font_title, fill=(255, 0, 0))
    draw.text((210, 111), user_data.get('displayName', 'N/A'), font=font_info, fill=(255, 255, 255))

    draw.text((100, 180), "Id:", font=font_title, fill=(0, 255, 255))
    draw.text((168, 189), user_data.get('userId', 'N/A'), font=font_info, fill=(255, 255, 255))

    draw.text((100, 260), "Username:", font=font_title, fill=(255, 255, 255))
    draw.text((350, 269), user_data.get('username', 'N/A'), font=font_info, fill=(255, 255, 255))

    draw.text((100, 340), "Số điện thoại:", font=font_title, fill=(255, 0, 255))
    draw.text((430, 349), user_data.get('phoneNumber', 'N/A'), font=font_info, fill=(255, 255, 255))

    draw.text((100, 420), "Giới tính:", font=font_title, fill=(255, 255, 0))
    draw.text((315, 433), {0: "Nam", 1: "Nữ"}.get(user_data.get('gender'), "Khác"), font=font_info, fill=(255, 255, 255))

    draw.text((100, 500), "Sinh nhật:", font=font_title, fill=(0, 255, 0))
    user_dob = user_data.get('dob')
    user_dob_str = datetime.fromtimestamp(user_dob).strftime('%d/%m/%Y') if user_dob else 'N/A'
    draw.text((333, 513), user_dob_str, font=font_info, fill=(255, 255, 255))

    draw.text((100, 580), "Tiểu sử:", font=font_title, fill=(255, 192, 203))
    bio_text = user_data.get('status', 'N/A')
    if len(bio_text) > 50:
        font_bio = ImageFont.truetype(fontc, 60)
    draw.text((290, 595), bio_text, font=font_bio, fill=(255, 255, 255))

    canvas_path = "output_canvas.png"
    background_image.save(canvas_path)
    return canvas_path

def handle_user_info(message, message_object, thread_id, thread_type, author_id, client):
    try:
        input_value = message.split()[1].lower() if len(message.split()) > 1 else author_id

        if message_object.mentions:
            input_value = message_object.mentions[0]['uid']

        user_id_data = client.fetchPhoneNumber(input_value, language="vi") or {}
        user_id_to_fetch = user_id_data.get('uid', input_value)
        sdob_to_fetch = user_id_data.get('sdob')

        user_info = client.fetchUserInfo(user_id_to_fetch) or {}
        user_data = user_info.get('changed_profiles', {}).get(user_id_to_fetch, {})

        canvas_path = create_canvas(user_data)

        if os.path.exists(canvas_path):
            client.sendLocalImage(
                canvas_path, 
                message=None,
                thread_id=thread_id,
                thread_type=thread_type,
                width=2323,
                height=1039
            )

            os.remove(canvas_path)

    except (ValueError, ZaloAPIException) as e:
        error_message = Message(text=f"Error: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"An unexpected error occurred: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'userinfo': handle_user_info
    }
