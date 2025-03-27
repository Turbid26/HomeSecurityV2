from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

KNOWN_FACES_FOLDER = 'known_faces'

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

if __name__ == '__main__':
    app.run(debug=True)