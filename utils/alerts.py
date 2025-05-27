import serial
import time
import firebase_admin
from firebase_admin import credentials, db
import requests

TELEGRAM_BOT_TOKEN = "7914841129:AAHFGtZ0ZZEmijsKhkU_3Z8Shv0fxXoOw1c"
TELEGRAM_CHAT_ID = "6825075764"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Initialize Firebase
def initialize_firebase():
    cred = credentials.Certificate("fb-admin.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ard-cloud-test-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

if not firebase_admin._apps:
    initialize_firebase()

def get_db_reference():
    """Returns Firebase database reference"""
    return db.reference()

def add_alert(alert_type, message):
    """Add a new alert to Firebase without overwriting existing ones."""
    ref = get_db_reference().child("alerts").child("zTnu554pvkUO1nsNJYPKxjO8nvB3")
    new_alert_ref = ref.push()
    alert_data = {
        "type": alert_type,
        "message": message,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    new_alert_ref.set(alert_data)
    
    print(f"Added alert: {alert_data}")
    telegram_message = f"Alert: {alert_data['type']}\nMessage: {alert_data['message']}\nTime: {alert_data['timestamp']}"
    send_telegram_message(telegram_message)

def send_telegram_message(message):
    """Send a notification to Telegram via the bot."""
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
    }
    response = requests.post(TELEGRAM_API_URL, data=payload)
    print(f"Telegram API response: {response.text}")
    if response.status_code == 200:
        print("Telegram message sent successfully!")
    else:
        print(f"Failed to send message. Error: {response.status_code}")