# helpers.py
import cv2
import face_recognition
import urllib.request
import numpy as np
from datetime import datetime
from utils.cloud_utils import upload_to_cloudinary
from utils.fb_config import firestore_db

camera = cv2.VideoCapture(1)

def gen_frames(user_email):
    known_face_encodings = get_known_face_encodings(user_email)

    while True:
        success, frame = camera.read()
        if not success:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        match_found = False
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            if any(matches):
                match_found = True
                
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        if not match_found and face_encodings:
            _, buffer = cv2.imencode('.jpg', frame)
            image_url = upload_to_cloudinary(
                image=buffer.tobytes(),
                name="Unknown",
                folder="HomeSec/Alerted/"
            )

            new_alert = {
                "image_url": image_url,
                "label": "Unknown",
                "timestamp": datetime.utcnow().isoformat(),
                "email": user_email
            }

            try:
                user_ref = firestore_db.collection('users').document(user_email)
                user_doc = user_ref.get()

                if not user_doc.exists:
                    print(f"No user found for {user_email}")
                    return

                # Get the current alerted_faces or initialize an empty list if not found
                user_data = user_doc.to_dict()
                alerted_faces = user_data.get("alerted_faces", [])
                
                # Add the new alert to the list
                alerted_faces.append(new_alert)

                # Update the user's alerted_faces field in Firestore
                user_ref.update({
                    "alerted_faces": alerted_faces,
                    "last_updated": datetime.utcnow().isoformat()
                })

                print(f"Alert added successfully for {user_email}")
            except Exception as e:
                print(f"Error updating Firestore: {e}")

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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
