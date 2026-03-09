from zlapi.models import Message
import requests
import os

def get_mitaizl():
    return {
        'thread': handle_thread_command
    }
