import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from bs4 import BeautifulSoup

# Load environment variables from security.env
load_dotenv("security.env")

# Get API credentials from environment variables
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# Ensure API credentials are properly set
if not api_id or not api_hash:
    raise ValueError("API credentials not found. Make sure security.env is set up correctly.")

# Convert API ID to integer (required by Telethon)
api_id = int(api_id)

# List of channels to extract messages from (without '@')
channels = ["UTMstudents", "mpputm", "utm_library"]

# Initialize Telegram client session
client = TelegramClient("session_name", api_id, api_hash)

with client:
    for channel in channels:
        print(f"Extracting messages from @{channel}...")

        # Get the latest 1000 messages from the channel
        messages = client.get_messages(channel, limit=1000)

        # Create HTML structure
        html = BeautifulSoup("""
        <html>
            <head><title>Exported Data</title></head>
            <body><div class='history'></div></body>
        </html>
        """, "html.parser")

        history_div = html.find("div", class_="history")

        # Add messages to the HTML file
        for msg in messages:
            if msg.text:
                msg_div = html.new_tag("div", **{"class": "message"})
                body_div = html.new_tag("div", **{"class": "body"})
                body_div.string = f"{msg.date.strftime('%Y-%m-%d %H:%M:%S')} - {msg.text}"
                msg_div.append(body_div)
                history_div.append(msg_div)

        # Save messages as an HTML file
        file_name = f"{channel}_messages.html"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(str(html.prettify()))

        print(f"Messages saved in {file_name}")

print("Extraction complete!")
