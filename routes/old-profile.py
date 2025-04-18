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

    return redirect(url_for('profile.profile'))@profile_bp.route('/update_surroundings', methods=['GET', 'POST'])
def update_surroundings():
    if 'user' not in session:
        return redirect(url_for('auth_bp.login'))

    user_id = session['user'].replace('.', '_')  # Ensure the user_id format is Firebase-friendly
    ref = get_realtime_db().child(f"SensorData/{user_id}")
    
    # Initialize settings with default empty values to avoid issues if no settings are present
    settings = {
        "device_name": "",
        "alert_motion": False,
        "alert_temp": False
    }

    if request.method == 'POST':
        # Get form data
        device_name = request.form.get("device_name")
        alert_motion = "alert_motion" in request.form
        alert_temp = "alert_temp" in request.form

        # Check if the device name is provided
        if not device_name:
            flash("⚠️ Please provide a device nickname.", "warning")
            return redirect(url_for('profile_bp.update_surroundings'))

        # Prepare the settings data to be saved
        settings = {
            "device_name": device_name,
            "alert_motion": alert_motion,
            "alert_temp": alert_temp
        }

        # Save the settings to Firebase
        try:
            ref.set(settings)
            flash("🏠 Home surroundings updated!", "success")
        except Exception as e:
            flash(f"⚠️ Failed to update surroundings. Error: {str(e)}", "error")
            return redirect(url_for('profile_bp.update_surroundings'))

        return redirect(url_for('profile_bp.profile'))

    elif request.method == 'GET':
        # Fetch the current settings from Firebase
        current_settings = ref.get()
        
        if current_settings:
            settings = current_settings.val()

        # Ensure 'settings' is always passed to the template
        return render_template('profile.html', settings=settings)
