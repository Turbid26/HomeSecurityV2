import time
from firebase_admin import db
from utils.alerts import add_alert  # This contains your add_alert() logic

TEMP_THRESHOLD = 40
GAS_THRESHOLD = 500

def monitor_sensor_data():
    ref = db.reference("/sensorData")
    
    while True:
        data = ref.get()
        if data:
            temperature = data.get("temperature", 0)
            gas = data.get("gas", 0)
            motion = data.get("motion", 0)

            if temperature > TEMP_THRESHOLD:
                add_alert("Temperature", f"High temperature: {temperature}°C")

            if gas > GAS_THRESHOLD:
                add_alert("Gas", f"Gas level too high: {gas}")

            if motion == 1:
                add_alert("Motion", "Motion detected")

        time.sleep(5)  # Poll every 5 seconds
