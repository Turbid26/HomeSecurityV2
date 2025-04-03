from flask import Flask, render_template,Response, request, jsonify, send_from_directory
import os
import cv2
from fb import get_db_reference

app = Flask(__name__)

KNOWN_FACES_FOLDER = 'known_faces'
camera = cv2.VideoCapture(0)

@app.route('/upload_faces')
def upload_faces():
    faces = os.listdir(KNOWN_FACES_FOLDER)  # List all files in known_faces directory
    return render_template('uploadface.html', faces=faces)

@app.route('/remove_face', methods=['POST'])
def remove_face():
    data = request.json
    face_path = os.path.join(KNOWN_FACES_FOLDER, data['face'])
    
    if os.path.exists(face_path):
        os.remove(face_path)
        return jsonify(success=True)
    
    return jsonify(success=False), 400

@app.route('/')
@app.route('/live')
def live_feed():
    return render_template('livefeed.html')

@app.route('/motion_status')
def motion_status():
    """Fetch motion status from Firebase"""
    ref = get_db_reference().child("sensorData/motion")
    motion = ref.get()
    return jsonify({"motion": motion})

def generate_frames():
    """Generate frames from the webcam"""
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Stream video feed when motion is detected"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

