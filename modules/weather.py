import requests
from zlapi.models import Message
from datetime import datetime, timedelta
import pytz
import time

des = {
    'version': "1.0.6",
    'credits': "Nguyễn Đức Tài",
    'description': "Xem thời tiết khu vực chỉ định"
}

apikey = "d7e795ae6a0d44aaa8abb1a0a7ac19e4"
vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')

def fetch_weather(area, retries=3):
    try:
        response = requests.get(
            f"https://api.accuweather.com/locations/v1/cities/search.json?q={requests.utils.quote(area)}&apikey={apikey}&language=vi-vn"
        )
        response.raise_for_status()
        data = response.json()

        if data:
            areaKey = data[0].get('Key')
        else:
            return "Không tìm thấy địa điểm này!"
    except requests.exceptions.RequestException:
        if retries > 0:
            time.sleep(1)
            return fetch_weather(area, retries - 1)
        return "Đã có lỗi xảy ra khi tìm địa điểm!"

    try:
        dataWeather = requests.get(
            f"http://api.accuweather.com/forecasts/v1/daily/10day/{areaKey}?apikey={apikey}&details=true&language=vi"
        )
        dataWeather.raise_for_status()
        dataWeather = dataWeather.json()
    except requests.exceptions.RequestException:
        if retries > 0:
            time.sleep(1)
            return fetch_weather(area, retries - 1)
        return "Đã có lỗi xảy ra khi lấy dữ liệu thời tiết!"

    def convert_F_to_C(F):
        return round((F - 32) / 1.8)

    dataWeatherDaily = dataWeather.get('DailyForecasts', [])
    if not dataWeatherDaily:
        return "Không có dữ liệu dự báo thời tiết!"

    dataWeatherToday = dataWeatherDaily[0]
    rainfall_amount = dataWeatherToday.get('Day', {}).get('Rain', {}).get('Value', 'Không có thông tin')
    rain_chance = dataWeatherToday.get('Day', {}).get('PrecipitationProbability', 'Không có thông tin')

    msg = (
        f"[ Thời tiết {area} ]\n"
        f"Thời tiết hôm nay:\n{dataWeather.get('Headline', {}).get('Text', 'Không có thông tin tiêu đề')}\n"
        f"🌡 Nhiệt độ thấp nhất - cao nhất: {convert_F_to_C(dataWeatherToday.get('Temperature', {}).get('Minimum', {}).get('Value', 0))}°C - {convert_F_to_C(dataWeatherToday.get('Temperature', {}).get('Maximum', {}).get('Value', 0))}°C\n"
        f"🌡 Nhiệt độ cảm nhận: {convert_F_to_C(dataWeatherToday.get('RealFeelTemperature', {}).get('Minimum', {}).get('Value', 0))}°C - {convert_F_to_C(dataWeatherToday.get('RealFeelTemperature', {}).get('Maximum', {}).get('Value', 0))}°C\n"
        f"🌧 Lượng mưa: {rainfall_amount} mm\n"
        f"☔ Xác suất mưa: {rain_chance}%\n"
        f"🌞 Ban ngày: {dataWeatherToday.get('Day', {}).get('LongPhrase', 'Không có thông tin')}\n"
        f"🌙 Ban đêm: {dataWeatherToday.get('Night', {}).get('LongPhrase', 'Không có thông tin')}"
    )
    return msg

def handle_weather_command(message, message_object, thread_id, thread_type, author_id, client):
    text = message.split()
    if len(text) < 2:
        error_message = Message(text="Vui lòng nhập khu vực cần xem thời tiết.")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    area = " ".join(text[1:])
    weather_info = fetch_weather(area)
    client.replyMessage(Message(text=f"{weather_info}"), message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'weather': handle_weather_command
    }
