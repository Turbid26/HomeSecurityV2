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

def read_serial():
    """Reads ESP32 data and sends it to Firebase"""
    try:
        ser = serial.Serial('COM7', 115200, timeout=1)  # Adjust to your port
        print("✅ Connected to ESP32")
    except serial.SerialException as e:
        print(f"❌ Serial connection failed: {e}")
        return

    while True:
        try:
            line = ser.readline().decode().strip()
            if line.startswith("T:"):
                parts = line.split(",")
                temperature = float(parts[0][2:])
                humidity = float(parts[1][2:])
                motion = int(parts[2][2:])
                gas = int(parts[3][2:])

                # Upload data to Firebase
                ref = get_db_reference().child("sensorData")
                ref.set({
                    "temperature": temperature,
                    "humidity": humidity,
                    "motion": motion,
                    "gas": gas
                })

                print(f"Data sent: Temp={temperature}, Humidity={humidity}, Motion={motion}, Gas={gas}")

                if temperature > 40:
                    add_alert("temperature", f"High Temperature Detected: {temperature}°C")

                if gas > 500:
                    add_alert("gas", f"Impuse gas levels exceeded threshold.")

                if motion == 1:
                    add_alert("motion", "Motion Detected at Entry")

        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(1)  # Prevent flooding errors

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


if __name__ == "__main__":
    read_serial()