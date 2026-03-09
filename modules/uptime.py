from zlapi.models import Message
import time
import os
import requests
import random
from PIL import Image, ImageDraw, ImageFont

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Xem thời gian bot hoạt động"
}

start_time = time.time()

def handle_uptime_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        current_time = time.time()
        uptime_seconds = int(current_time - start_time)

        days = uptime_seconds // (24 * 3600)
        uptime_seconds %= (24 * 3600)
        hours = uptime_seconds // 3600
        uptime_seconds %= 3600
        minutes = uptime_seconds // 60
        seconds = uptime_seconds % 60

        uptime_message = f"{days} Ngày, {hours} giờ, {minutes} phút, {seconds} giây."
        message_to_send = Message(text=uptime_message)

        # choose a background URL if you want an online picture; otherwise keep None
        bg_url = "https://jpeg.org/images/jpeg2000-home.jpg"  # e.g. "https://jpeg.org/images/jpeg2000-home.jpg"

        # generate the canvas, optionally passing the URL
        generate_canvas_image(uptime_message, bg_url)

        # local image path (unchanged)
        image_path = "modules/cache/uptime.jpeg"

        if os.path.exists(image_path):
            client.sendLocalImage(
                image_path, 
                message=None,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1920,
                height=1080
            )

            try:
                os.remove(image_path)
            except OSError:
                pass
        else:
            raise Exception("Không thể lưu ảnh")

    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

from io import BytesIO


def generate_canvas_image(uptime_message, background_url=None):
    # load background either from a remote URL or local file
    if background_url:
        resp = requests.get(background_url)
        resp.raise_for_status()
        background = Image.open(BytesIO(resp.content))
    else:
        background = Image.open("modules/cache/bg.jpg")

    width, height = background.size

    draw = ImageDraw.Draw(background)

    # helper to adjust font size until text fits within width
    def fit_font(text, font_path, initial_size, max_width):
        size = initial_size
        while size > 8:  # avoid going to absurdly small sizes
            try:
                f = ImageFont.truetype(font_path, size)
            except IOError:
                return ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=f)
            text_width = bbox[2] - bbox[0]
            if text_width <= max_width:
                return f
            size -= 2
        return ImageFont.load_default()

    font_path = "modules/cache/UTM-AvoBold.ttf"
    # compute available width (leave some horizontal margin)
    margin = 40
    avail_width = width - 2 * margin

    # choose initial sizes and then shrink if necessary
    font = fit_font("THỜI GIAN BOT ĐÃ ONLINE", font_path, 60, avail_width)
    font_time = fit_font(uptime_message, font_path, 90, avail_width)

    gradient_colors = [generate_random_color(), generate_random_color()]
    gradient_colors2 = [generate_random_color(), generate_random_color()]

    text1 = "THỜI GIAN BOT ĐÃ ONLINE"
    text2 = uptime_message

    text1_bbox = draw.textbbox((0, 0), text1, font=font)
    text2_bbox = draw.textbbox((0, 0), text2, font=font_time)

    text1_width = text1_bbox[2] - text1_bbox[0]
    text1_height = text1_bbox[3] - text1_bbox[1]

    text2_width = text2_bbox[2] - text2_bbox[0]
    text2_height = text2_bbox[3] - text2_bbox[1]

    text1_x = (width - text1_width) // 2
    text1_y = 50

    text2_x = (width - text2_width) // 2
    text2_y = (height - text2_height) // 2

    apply_gradient(draw, text1, font, (text1_x, text1_y), gradient_colors)

    apply_gradient(draw, text2, font_time, (text2_x, text2_y), gradient_colors2)

    background.save("modules/cache/uptime.jpeg")

def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def mix_colors(color1, color2, factor):
    r = int(color1[0] * (1 - factor) + color2[0] * factor)
    g = int(color1[1] * (1 - factor) + color2[1] * factor)
    b = int(color1[2] * (1 - factor) + color2[2] * factor)
    return (r, g, b)

def apply_gradient(draw, text, font, start_pos, gradient_colors, shadow_offset=(3, 3), shadow_blur_radius=5):
    total_width = draw.textbbox((0, 0), text, font=font)[2] - draw.textbbox((0, 0), text, font=font)[0]
    num_chars = len(text)

    for i, char in enumerate(text):
        char_width = draw.textbbox((0, 0), char, font=font)[2] - draw.textbbox((0, 0), char, font=font)[0]
        pos = start_pos[0] + sum([draw.textbbox((0, 0), text[j], font=font)[2] - draw.textbbox((0, 0), text[j], font=font)[0] for j in range(i)])
        
        shadow_pos = (pos + shadow_offset[0], start_pos[1] + shadow_offset[1])
        draw.text(shadow_pos, char, font=font, fill=(0, 0, 0, 255))

    for i, char in enumerate(text):
        char_width = draw.textbbox((0, 0), char, font=font)[2] - draw.textbbox((0, 0), char, font=font)[0]
        pos = start_pos[0] + sum([draw.textbbox((0, 0), text[j], font=font)[2] - draw.textbbox((0, 0), text[j], font=font)[0] for j in range(i)])

        factor = i / num_chars
        color = mix_colors(gradient_colors[0], gradient_colors[1], factor)

        draw.text((pos, start_pos[1]), char, font=font, fill=color)

def get_mitaizl():
    return {
        'uptime': handle_uptime_command
    }
