import cloudinary
import cloudinary.uploader
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

cloudinary.config(
    cloud_name="duhho2j3z",
    api_key="379375491312472",
    api_secret="GyL_L3BGlKNXMtMyV_ciSvioftU"
)

app = Flask(__name__)

# Firebase config
cred = credentials.Certificate("fb-admin.json")  # your Firebase service account
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/upload", methods=["GET", "POST"])
def upload():
    user_email = 'test-email@gmail.com'  # or session['user_email']

    if request.method == "POST":
        image = request.files.get("image")
        name = request.form.get("name")
        timestamp = datetime.utcnow().isoformat()

        if image:
            # Upload to Cloudinary under 'known/' folder
            result = cloudinary.uploader.upload(
                image,
                folder="HomeSec/Known/",
                public_id=f"{name}_{int(datetime.utcnow().timestamp())}", 
                overwrite=True,
                resource_type="image"
            )

            image_url = result["secure_url"]

            # Check if user exists
            user_doc_ref = db.collection("users").document(user_email)
            user_doc = user_doc_ref.get()

            if user_doc.exists:
                user_data = user_doc.to_dict()
                known_faces = user_data.get("known_faces", [])
                known_faces.append(image_url)
                user_doc_ref.update({
                    "known_faces": known_faces,
                    "last_updated": timestamp
                })
            else:
                db.collection("users").document(user_email).set({
                    "email": user_email,
                    "known_faces": [image_url],
                    "alerted_faces": [],
                    "last_updated": timestamp
                })

            return redirect(url_for("upload"))

    # Get known faces for this user
    user_doc = db.collection("users").document(user_email).get()
    known_faces = []
    if user_doc.exists:
        known_faces = user_doc.to_dict().get("known_faces", [])

    return render_template("upload.html", faces=known_faces)

@app.route("/remove_face", methods=["POST"])
def remove_face():
    user_email = 'test-email@gmail.com'
    face_url = request.json.get("face")

    user_ref = db.collection("users").document(user_email)
    user_doc = user_ref.get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
        known_faces = user_data.get("known_faces", [])
        if face_url in known_faces:
            known_faces.remove(face_url)
            user_ref.update({
                "known_faces": known_faces,
                "last_updated": datetime.utcnow().isoformat()
            })
            return jsonify(success=True)

    return jsonify(success=False)

if __name__ == '__main__':
    app.run(debug=True)