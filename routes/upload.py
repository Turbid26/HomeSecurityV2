from flask import Blueprint, request, redirect, render_template, session, url_for
import cloudinary.uploader
from datetime import datetime
from utils.fb_config import firestore_db
from utils.cloud_utils import upload_to_cloudinary

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():
    user_email = session['user']

    if request.method == "POST":
        image = request.files.get("image")
        name = request.form.get("name")
        role = request.form.get("role")  # "family" or "guest"
        start_time = request.form.get("start_time")
        expiry_time = request.form.get("expiry_time")

        if image:
            image_url = upload_to_cloudinary(image, name)

            face_entry = {
                "url": image_url,
                "name": name,
                "role": role,
                "added_on": datetime.utcnow().isoformat()
            }

            if role == "guest":
                face_entry["start_time"] = start_time
                face_entry["expiry_time"] = expiry_time
            else:
                face_entry["start_time"] = None
                face_entry["expiry_time"] = None

            # Save to Firestore
            user_ref = firestore_db.collection("users").document(user_email)
            user_doc = user_ref.get()

            if user_doc.exists:
                faces = user_doc.to_dict().get("known_faces", [])
                faces.append(face_entry)
                user_ref.update({
                    "known_faces": faces,
                    "last_updated": datetime.utcnow().isoformat()
                })
            else:
                user_ref.set({
                    "email": user_email,
                    "known_faces": [face_entry],
                    "alerted_faces": [],
                    "last_updated": datetime.utcnow().isoformat()
                })

            return redirect(url_for("upload_bp.upload"))

    #remove guests if time is up
    remove_expired_guests(user_email)
    
    # Render template with known faces
    user_doc = firestore_db.collection("users").document(user_email).get()
    known_faces = user_doc.to_dict().get("known_faces", []) if user_doc.exists else []
    return render_template("upload.html", faces=known_faces)


def remove_expired_guests(user_email):
    user_ref = firestore_db.collection("users").document(user_email)
    user_doc = user_ref.get()

    if not user_doc.exists:
        return

    user_data = user_doc.to_dict()
    known_faces = user_data.get("known_faces", [])
    updated_faces = []

    now = datetime.utcnow()

    for face in known_faces:
        if face.get("role") == "guest":
            expiry_str = face.get("expiry_time")
            if expiry_str:
                try:
                    expiry_time = datetime.strptime(expiry_str, "%Y-%m-%dT%H:%M")
                    print(expiry_time, "  ", now)
                    print(expiry_time - now)
                    if expiry_time < now:
                        updated_faces.append(face)
                    else:
                        print(f"Removing expired guest: {face.get('name')}")
                except ValueError:
                    print(f"Invalid expiry_time for face: {face.get('name')}")
        else:
            updated_faces.append(face)


    # Only update if something changed
    if len(updated_faces) != len(known_faces):
        user_ref.update({"known_faces": updated_faces})