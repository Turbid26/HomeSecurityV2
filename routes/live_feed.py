from flask import Blueprint, render_template, jsonify, session, redirect, url_for, Response
import cv2
from firebase_admin import db

live_feed_bp = Blueprint('live_feed_bp', __name__)

camera = cv2.VideoCapture(1)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield frame in proper format for HTML5 video streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@live_feed_bp.route('/live', methods=['GET'])
def live_feed():
    if 'user' not in session:
        return redirect(url_for('auth_bp.login'))
    return render_template('livefeed.html')

@live_feed_bp.route('/live_data', methods=['GET'])
def live_data():
    try:
        ref = db.reference("sensorData")
        data = ref.get()
        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "No data available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@live_feed_bp.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')