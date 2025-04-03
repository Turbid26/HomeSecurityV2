import serial
import time
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
def initialize_firebase():
    cred = credentials.Certificate("ard-cloud-test-firebase-adminsdk-fbsvc-36cea9ff3a.json")
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
        ser = serial.Serial('COM12', 115200, timeout=1)  # Adjust to your port
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

                # Upload data to Firebase
                ref = get_db_reference().child("sensorData")
                ref.set({
                    "temperature": temperature,
                    "humidity": humidity,
                    "motion": motion
                })

                print(f"Data sent: Temp={temperature}, Humidity={humidity}, Motion={motion}")

                if temperature > 40:
                    add_alert("temperature", f"High Temperature Detected: {temperature}°C")

                if motion == 1:
                    add_alert("motion", "Motion Detected at Entryway")

        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(1)  # Prevent flooding errors

def add_alert(alert_type, message):
    """Add a new alert to Firebase without overwriting existing ones."""
    ref = get_db_reference().child("alerts")
    new_alert_ref = ref.push()
    alert_data = {
        "type": alert_type,
        "message": message,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    new_alert_ref.set(alert_data)
    
    print(f"Added alert: {alert_data}")

if __name__ == "__main__":
    read_serial()
