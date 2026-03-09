import random
from zlapi.models import Message

des = {
    'version': "1.0.5",
    'credits': "Nguyễn Đức Tài",
    'description': "gọi bot"
}

goibot_responses = [
    "em đây", "gọi cc", "bot nghe", "gọi lồn gọi lắm", "đi ỉa đi vui lắm", 
    "tao cười tao ỉa", "bé nghe", "có bot", "gọi gì nói đi", "m hết trò à", 
    "gọi không nói", "gọi cặc", "cái gì", "sủa em", "clj", "cắn mạnh đi em", 
    "nói liên tục", "cắn liên tục đi em"
]

def goibot(message, message_object, thread_id, thread_type, author_id, client):
    response = random.choice(goibot_responses)
    gui = Message(text=response)
    client.replyMessage(gui, message_object, thread_id, thread_type)

def get_mitaizl():
    return dict.fromkeys(
        ['bot', 'bót'], goibot
    )
