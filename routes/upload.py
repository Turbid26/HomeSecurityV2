from flask import Blueprint, request, redirect, render_template, session, url_for
import cloudinary.uploader
from datetime import datetime
from utils.fb_config import firestore_db
from utils.cloud_utils import upload_to_cloudinary

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():
    user_email = session['user']
    #user_email = 'test-email@gmail.com'

    if request.method == "POST":
        image = request.files.get("image")
        name = request.form.get("name")

        if image:
            image_url = upload_to_cloudinary(image, name)
            # Save to Firestore
            user_ref = firestore_db.collection("users").document(user_email)
            user_doc = user_ref.get()

            if user_doc.exists:
                faces = user_doc.to_dict().get("known_faces", [])
                faces.append(image_url)
                user_ref.update({
                    "known_faces": faces,
                    "last_updated": datetime.utcnow().isoformat()
                })
            else:
                user_ref.set({
                    "email": user_email,
                    "known_faces": [image_url],
                    "alerted_faces": [],
                    "last_updated": datetime.utcnow().isoformat()
                })
            return redirect(url_for("upload_bp.upload"))

    # Render template with known faces
    user_doc = firestore_db.collection("users").document(user_email).get()
    known_faces = user_doc.to_dict().get("known_faces", []) if user_doc.exists else []
    return render_template("upload.html", faces=known_faces)
