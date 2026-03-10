from zlapi.models import *
import time
from concurrent.futures import ThreadPoolExecutor
import threading
import os

des = {
    'version': "1.0.0",
    'credits': "Nguyen Duc Tai",
    'description': "Xem ping của bot"
}
def handel_ping_command(message, message_object, thread_id, thread_type, author_id, client):
        start_time = time.time()
        pingmark = "Ping: "
        client.sendReaction(messageObject=message_object, reactionIcon=pingmark, thread_id=thread_id, thread_type=thread_type)

        end_time = time.time()
        ping_time = end_time - start_time

        ping = f"{1000 * ping_time:.4f}ms"
        client.sendReaction(messageObject=message_object, reactionIcon=ping, thread_id=thread_id, thread_type=thread_type)

def get_mitaizl():
    return {
    'ping': handel_ping_command
    }
