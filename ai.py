import requests
import json
import os # Import the os module for path operations and directory creation
from zlapi.models import *
from config import *

description = {
    "name": "ai",
    "version": "1.0",
    "credits": "ereDLT",
    "description": "Nói chuyện với AI",
    "admin": False,
    "ad_t": False
}
# Global dictionary to store chat histories.
# The key will be a tuple: (thread_id, author_id)
# This ensures a unique conversation history for each user within each specific chat thread.
chat_histories = {}

# Define the maximum number of message turns to keep in memory.
# For example, 10 means approx. 5 user messages and 5 bot responses (plus the persona prompt).
MAX_HISTORY_LENGTH = 10 

# The initial persona prompt to be sent once per new conversation thread for a specific user.
INITIAL_PERSONA_PROMPT = "prompt"

# Define the directory where history files will be stored
# Make sure this path is correct relative to where your bot script runs
HISTORY_DIR = "modules/data/history"

# Ensure the history directory exists
os.makedirs(HISTORY_DIR, exist_ok=True)

def get_history_file_path(thread_id, author_id):
    """Generates the file path for a specific user's history in a thread."""
    # Using .json extension as we will save JSON data
    return os.path.join(HISTORY_DIR, f"{thread_id}_{author_id}.json")

def load_history_from_file(file_path):
    """Loads chat history from a JSON file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Lỗi đọc lịch sử từ file {file_path}: {e}. Khởi tạo lịch sử mới.")
            return []
    return []

def save_history_to_file(file_path, history):
    """Saves chat history to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Lỗi ghi lịch sử vào file {file_path}: {e}")

def handle_ai(self, message, thread_id, thread_type, author_id, message_object):
    """
    Handles messages starting with 'a', sends them to the Gemini API,
    and maintains conversation history for each user within each thread.
    """
    text_parts = message.split()
    user_query = " ".join(text_parts[1:])
    if user_query == "tắt" and author_id in ADMIN:
        self.send(Message(text=f";ex"), thread_id, thread_type, ttl=10000)
        return

    # Create a unique key for this user's conversation in this thread
    history_key = (thread_id, author_id)
    file_path = get_history_file_path(thread_id, author_id)

    # --- Conversation History Management ---
    # Get the chat history for the current user in this thread.
    # If not in memory, try loading from file. If neither, initialize.
    if history_key not in chat_histories:
        current_chat_history = load_history_from_file(file_path)
        
        # If the loaded history is empty (new conversation for this user in this thread)
        # and it's not just a file read error, add the initial persona prompt.
        # We check if it's empty to ensure the persona is only added once.
        if not current_chat_history: 
            current_chat_history.append({
                "role": "user",
                "parts": [
                    {
                        "text": INITIAL_PERSONA_PROMPT
                    }
                ]
            })
        chat_histories[history_key] = current_chat_history
    else:
        current_chat_history = chat_histories[history_key]

    # Add the user's current message to the conversation history.
    current_chat_history.append({
        "role": "user",
        "parts": [
            {
                "text": user_query 
            }
        ]
    })

    # --- Limit History Length ---
    # To prevent history from growing indefinitely and making API requests too large,
    # we keep only the most recent messages up to MAX_HISTORY_LENGTH.
    if len(current_chat_history) > MAX_HISTORY_LENGTH:
        current_chat_history = current_chat_history[-MAX_HISTORY_LENGTH:]
        chat_histories[history_key] = current_chat_history # Update in-memory history

    # --- Debugging: Print current history before API call ---
    print(f"\n--- Lịch sử trò chuyện hiện tại cho {author_id} trong nhóm {thread_id} ---")
    print(json.dumps(current_chat_history, indent=2, ensure_ascii=False))
    print("------------------------------------------------------------------\n")
    # --- End Debugging ---


    # --- Gemini API Configuration ---
    api_key = "AIzaSyC_rUK8mEpykaWgU2Ut_URC0uFEyBJFlRU"  
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    headers = {
        'Content-Type': 'application/json'
    }

    # The 'contents' of the API request now include the entire conversation history.
    data = {
        "contents": current_chat_history
    }

    # --- API Call and Response Handling ---
    response = None 
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() 
        
        response_data = response.json()
        # print(json.dumps(response_data, indent=2)) # Print full response for debugging

        bot_response_text = response_data['candidates'][0]['content']['parts'][0]['text']

        # Add the bot's response to the conversation history
        current_chat_history.append({
            "role": "model",
            "parts": [
                {
                    "text": bot_response_text
                }
            ]
        })
        chat_histories[history_key] = current_chat_history # Update in-memory history

        # Save the updated history to file after successful API call
        save_history_to_file(file_path, current_chat_history)

        self.send(Message(text=f"{bot_response_text}"), thread_id, thread_type, ttl=120000)

    except requests.exceptions.RequestException as e:
        print(f"Lỗi trong quá trình gọi API: {e}")
        if response is not None:
            print(f"Mã trạng thái phản hồi: {response.status_code}")
            print(f"Nội dung phản hồi: {response.text}")
        
        # If API call fails, remove the last user message from history
        # to avoid sending an incomplete turn in the next attempt.
        if current_chat_history and current_chat_history[-1]["role"] == "user":
            current_chat_history.pop()
            chat_histories[history_key] = current_chat_history 
            # It's also good to try saving the history without the failed user message
            save_history_to_file(file_path, current_chat_history)

# --- Bot Command Setup ---
def setup_command(bot_instance):
    return {
        "ai": handle_ai
    }

# --- Bot Description (Metadata) ---
