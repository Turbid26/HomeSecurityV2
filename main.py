from flask import Flask, render_template, jsonify, Response
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

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

@app.route('/')
@app.route('/live')
def live_feed():
    """Render Live Feed Page"""
    return render_template('livefeed.html')


@app.route('/live_data')
def live_data():
    """Fetch sensor data from Firebase"""
    ref = db.reference("sensorData")
    data = ref.get()

    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "No data available"}), 404

@app.route('/home_alerts')
def home_alerts():
    """Render the Home Alerts page."""
    return render_template('homealerts.html')

@app.route('/alerts_data')
def alerts_data():
    """Fetch sensor data from Firebase to display alerts"""
    ref = db.reference("sensorData")
    data = ref.get()

    if data:
        return jsonify({
            "motion": data.get("motion", 0),
            "temperature": data.get("temperature", 0)
        })
    else:
        return jsonify({"error": "No data available"}), 404


if __name__ == '__main__':
    app.run(debug=True)
