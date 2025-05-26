import cv2
import numpy as np
import urllib.request
from datetime import datetime, timedelta
import time
import requests

from utils.cloud_utils import upload_to_cloudinary
from utils.fb_config import firestore_db

import insightface

ALERT_INTERVAL = timedelta(seconds=30)
last_alert_time = datetime.min

ESP32_STREAM_URL = "http://192.168.68.114:81/stream"
camera = cv2.VideoCapture(ESP32_STREAM_URL)

TELEGRAM_BOT_TOKEN = "7914841129:AAHFGtZ0ZZEmijsKhkU_3Z8Shv0fxXoOw1c"
TELEGRAM_CHAT_ID = "6825075764"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# TARGET_FPS = 10
# FRAME_DURATION = 1.0 / TARGET_FPS

# Initialize InsightFace model (FaceAnalysis)
model = insightface.app.FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
model.prepare(ctx_id=0)  # CPU context

def get_known_face_encodings(user_email):
    try:
        user_ref = firestore_db.collection('users').document(user_email)
        user_doc = user_ref.get()
        if not user_doc.exists:
            print(f"No user found for {user_email}")
            return []

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

                # InsightFace expects BGR images, no need to convert color space here
                faces = model.get(img)
                if len(faces) > 0:
                    # Use embedding of first face found
                    embedding = faces[0].embedding
                    encodings.append(embedding)
            except Exception as e:
                print(f"Error processing known face URL: {url} — {e}")
                continue

        return encodings

    except Exception as e:
        print(f"Error retrieving known faces: {e}")
        return []

def gen_frames(user_email):
    global last_alert_time
    global camera

    known_face_encodings = get_known_face_encodings(user_email)

    while True:
        start_time = time.time()
        success, frame = read_latest_frame(camera)
        if not success:
            print("Frame read failed. Reconnecting...")
            camera.release()
            time.sleep(2)
            camera = cv2.VideoCapture(ESP32_STREAM_URL)
            continue

        # Run face detection + recognition on full frame (or resize if needed)
        faces = model.get(frame)  # returns list of Face objects with bbox and embedding

        match_found = False

        for face in faces:
            bbox = face.bbox.astype(int)  # [left, top, right, bottom]
            embedding = face.embedding

            # Compare embedding with known faces (cosine similarity)
            if known_face_encodings:
                sims = [np.dot(embedding, known_emb) / (np.linalg.norm(embedding)*np.linalg.norm(known_emb)) for known_emb in known_face_encodings]
                max_sim = max(sims)
                threshold = 0.5  # adjust threshold based on accuracy vs recall tradeoff
                if max_sim > threshold:
                    match_found = True
                    left, top, right, bottom = bbox
                    cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        if not match_found and len(faces) > 0:
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

                    message_text = f"🚨 Unknown face detected at {now.isoformat()}! Image URL: {image_url}"
                    send_telegram_message(message_text)

                    last_alert_time = now

                    last_alert_time = now

                except Exception as e:
                    print(f"Error updating Firestore: {e}")

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        # elapsed = time.time() - start_time
        # if elapsed < FRAME_DURATION:
        #     time.sleep(FRAME_DURATION - elapsed)


def send_telegram_message(text):
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        response = requests.post(TELEGRAM_API_URL, data=data)
        if response.status_code != 200:
            print(f"Telegram API error: {response.text}")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def read_latest_frame(camera):
    """
    Grab and discard all buffered frames, returning only the most recent one.
    """
    grabbed = False
    frame = None
    while True:
        ret, temp_frame = camera.read()
        if not ret:
            break
        grabbed = True
        frame = temp_frame
    return grabbed, frame