from flask import Blueprint, render_template, session
from firebase_admin import firestore

activities_bp = Blueprint('activities', __name__)
db = firestore.client()

@activities_bp.route('/recent_activities')
def recent_activities():
    user = session.get('user')  # Assuming you're storing the logged-in user ID in session
    if not user:
        return "User not logged in", 401

    print(user)
    user_doc = db.collection('users').document(user).get()
    if not user_doc.exists:
        return "User data not found", 404

    user_data = user_doc.to_dict()
    alerted_faces = user_data.get('alerted_faces', [])

    # Sort by timestamp, newest first
    alerted_faces.sort(key=lambda x: x['timestamp'], reverse=True)

    return render_template('recent_activities.html', faces=alerted_faces)
