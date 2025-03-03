import json
import os

DB_FILE = "chat_data.json"

def load_chats():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return {}

def save_chats(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file)

def get_chat_history(chat_id):
    chats = load_chats()
    return chats.get(chat_id, {"name": "Default", "messages": []})

def save_chat_message(chat_id, message):
    chats = load_chats()
    if chat_id not in chats:
        chats[chat_id] = {"name": "Default", "messages": []}
    chats[chat_id]["messages"].append(message)
    save_chats(chats)
