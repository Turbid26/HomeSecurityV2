from flask import Blueprint, request, jsonify, session
from utils.fb_config import firestore_db
from datetime import datetime
from utils.cloud_utils import delete_from_cloudinary, extract_id_from_url  # Optional, if you want to delete from Cloudinary

remove_bp = Blueprint('remove_bp', __name__)

@remove_bp.route("/remove_face", methods=["POST"])
def remove_face():
    user_email = session['user']
    #user_email = 'test-email@gmail.com'
    if not user_email:
        return jsonify(success=False, message="User not logged in")

    face_url = request.json.get("face")
    if not face_url:
        return jsonify(success=False, message="No face URL provided")

    user_ref = firestore_db.collection("users").document(user_email)
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

            # Optional: Remove from Cloudinary
            public_id = extract_id_from_url(face_url)
            delete_from_cloudinary(public_id)

            return jsonify(success=True)

    return jsonify(success=False, message="Face not found")
