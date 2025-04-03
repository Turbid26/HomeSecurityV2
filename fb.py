import serial
import firebase_admin
import threading
from firebase_admin import credentials, db
import time

# Firebase Initialization (only runs once)
def initialize_firebase():
    cred = credentials.Certificate("ard-cloud-test-firebase-adminsdk-fbsvc-36cea9ff3a.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ard-cloud-test-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Ensure Firebase is initialized only once
if not firebase_admin._apps:
    initialize_firebase()

def get_db_reference():
    """Returns the Firebase database reference"""
    return db.reference()

def read_serial():
    time.sleep(2)
    ser = serial.Serial('COM5', 115200, timeout=1)  # Adjust to your COM port

    while True:
        try:
            line = ser.readline().decode().strip()
            if line.startswith("T:"):
                parts = line.split(",")
                temperature = float(parts[0][2:])  # Extract temperature
                humidity = float(parts[1][2:])  # Extract humidity
                motion = int(parts[2][2:])  # Extract motion status

                # Send data to Firebase
                ref = get_db_reference().child("sensorData")
                ref.set({
                    "temperature": temperature,
                    "humidity": humidity,
                    "motion": motion
                })

                print(f"Data sent: Temp={temperature}, Humidity={humidity}, Motion={motion}")

        except Exception as e:
            print(f"Error: {e}")

# Run serial reading in a separate thread
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()
