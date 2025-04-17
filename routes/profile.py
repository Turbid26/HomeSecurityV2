from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import pyrebase
import json
from utils.fb_config import get_realtime_db

profile_bp = Blueprint('profile_bp', __name__)

with open('fb-nonadmin.json') as f:
    firebaseConfig = json.load(f)

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@profile_bp.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('auth_bp.login'))
    return render_template('profile.html')

@profile_bp.route('/change_password', methods=['POST'])
def change_password():
    if 'user' not in session:
        return redirect(url_for('auth_bp.login'))

    email = session['user']
    try:
        auth.send_password_reset_email(email)
        flash("🔐 Password reset email sent!", "success")
    except:
        flash("⚠️ Failed to send reset email. Try again later.", "error")

    return redirect(url_for('profile.profile'))

@profile_bp.route('/update_surroundings', methods=['POST'])
def update_surroundings():
    if 'user' not in session:
        return redirect(url_for('auth_bp.login'))

    user_id = session['user'].replace('.', '_')  # or however you're storing users
    ref = get_realtime_db().child(f"SensorData/{user_id}")

    settings = {
        "device_name": request.form.get("device_name"),
        "alert_motion": "alert_motion" in request.form,
        "alert_temp": "alert_temp" in request.form,
    }

    ref.set(settings)
    flash("🏠 Home surroundings updated!", "success")
    return redirect(url_for('profile_bp.profile'))
