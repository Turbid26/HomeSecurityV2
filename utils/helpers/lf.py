# helpers.py
import cv2
import face_recognition
import urllib.request
import numpy as np
from datetime import datetime
from utils.cloud_utils import upload_to_cloudinary
from utils.fb_config import firestore_db
import time
from datetime import datetime, timedelta

ALERT_INTERVAL = timedelta(seconds=30)
last_alert_time = datetime.min

ESP32_STREAM_URL = "http://192.168.68.107:81/stream"
#ESP32_STREAM_URL = 1
camera = cv2.VideoCapture(ESP32_STREAM_URL)

TARGET_FPS = 10
FRAME_DURATION = 1.0 / TARGET_FPS

def gen_frames(user_email):
    global camera 

    ALERT_INTERVAL = timedelta(seconds=30)
    last_alert_time = datetime.min
    known_face_encodings = get_known_face_encodings(user_email)
    print(f"Loaded {len(known_face_encodings)} known face encodings")

    while True:  # Wrap in list to make it mutable

        start_time = time.time()
        success, frame = camera.read()
        if not success:
            print("Frame read failed. Reconnecting...")
            camera.release()
            time.sleep(2)
            camera = cv2.VideoCapture(ESP32_STREAM_URL)
            continue

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        match_found = False
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            if any(matches):
                print("inside")
                match_found = True

                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  # Green rectangle


        if not match_found and face_encodings:
            now = datetime.utcnow()
            if now - last_alert_time >= ALERT_INTERVAL:
                _, buffer = cv2.imencode('.jpg', frame)
                image_url = upload_to_cloudinary(
                    image=buffer.tobytes(),
                    name="Unknown",
                    folder="HomeSec/Alerted/"
                )

                new_alert = {
                    "image_url": image_url,
                    "label": "Unknown",
                    "timestamp": now.isoformat(),
                    "email": user_email
                }

                try:
                    user_ref = firestore_db.collection('users').document(user_email)
                    user_doc = user_ref.get()

                    if not user_doc.exists:
                        print(f"No user found for {user_email}")
                        return

                    user_data = user_doc.to_dict()
                    alerted_faces = user_data.get("alerted_faces", [])
                    alerted_faces.append(new_alert)

                    user_ref.update({
                        "alerted_faces": alerted_faces,
                        "last_updated": now.isoformat()
                    })

                    print(f"Alert added successfully for {user_email}")
                    last_alert_time = now  # ✅ Update the last alert time

                except Exception as e:
                    print(f"Error updating Firestore: {e}")

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        elapsed = time.time() - start_time
        if elapsed < FRAME_DURATION:
            time.sleep(FRAME_DURATION - elapsed)

def get_known_face_encodings(user_email):

    try:
        # Access Firestore user document
        user_ref = firestore_db.collection('users').document(user_email)
        user_doc = user_ref.get()

        if not user_doc.exists:
            print(f"No user found for {user_email}")
            return []

        # Get the known_faces field
        known_faces = user_doc.to_dict().get("known_faces", [])
        if not known_faces:
            print(f"No known faces found for {user_email}")
            return []

        encodings = []
        for face in known_faces:
            url = face.get("url")
            if not url:
                continue

            try:
                resp = urllib.request.urlopen(url)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                img = cv2.imdecode(image, cv2.IMREAD_COLOR)
                face_encoding = face_recognition.face_encodings(img)
                if face_encoding:
                    encodings.append(face_encoding[0])
            except Exception as e:
                print(f"Error processing known face URL: {url} — {e}")
                continue

        return encodings
    
    except Exception as e:
        print(f"Error retrieving known faces: {e}")
        return []
