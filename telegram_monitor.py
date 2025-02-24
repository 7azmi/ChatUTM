from telethon import TelegramClient, events
from pymongo import MongoClient
import datetime

# Telegram API Credentials
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))  # Replace with your Telegram API ID stored in .env
API_HASH = os.getenv("TELEGRAM_API_HASH")     # Replace with your Telegram API Hash stored in .env
PHONE_NUMBER = os.getenv("TELEGRAM_PHONE_NUMBER")  # Your Telegram phone number stored in .env

# MongoDB Connection
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client.telegram_data  # Database Name
messages_collection = db.messages  # Collection Name

# List of Groups & Channels to Monitor
CHANNELS_AND_GROUPS = [
    "@UTMstudents",
    "@mpputm",
    "@ugfcutm",
    "@utm_library"
]

# Initialize Telegram Client
client = TelegramClient("user_session", API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNELS_AND_GROUPS))
async def new_message_handler(event):
    """Handle new messages from monitored groups & channels and save them to MongoDB."""
    message_data = {
        "chat_id": event.chat_id,
        "chat_title": event.chat.title if event.chat else "Unknown",
        "sender_id": event.sender_id,
        "message_text": event.raw_text,
        "timestamp": datetime.datetime.utcnow()
    }
    
    # Save the message to MongoDB
    messages_collection.insert_one(message_data)
    
    print(f"📩 New Message from {message_data['chat_title']}: {message_data['message_text']}")

# Start Client
async def main():
    await client.start(PHONE_NUMBER)
    print("🚀 Listening for new messages in groups & channels (with MongoDB)...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
