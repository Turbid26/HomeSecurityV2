from flask import Flask, render_template, jsonify, Response
import firebase_admin
from firebase_admin import credentials, db
import cv2

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


camera = cv2.VideoCapture(0)  # Open default webcam

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


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

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
