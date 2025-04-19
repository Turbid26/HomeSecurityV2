from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import pyrebase
import json
from utils.fb_config import get_realtime_db
from firebase_admin import db

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

@profile_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user' not in session:
        return redirect(url_for('auth_bp.login'))
    return render_template('profile_sub/change_password.html')

@profile_bp.route('/update_surroundings', methods=['GET', 'POST'])
def update_surroundings():
    if 'user' not in session:
        return redirect(url_for('auth_bp.login'))

    # Reference to root 'sensorData' in Firebase
    #ref = get_realtime_db().child("sensorData")
    ref = db.reference("sensorData")
    print(ref.get())
    # If the request is GET, fetch the current sensor data
    if request.method == 'GET':
        try:
            settings = ref.get()  # Fetch the current settings from Firebase
        except Exception as e:
            flash(f"⚠️ Failed to load home details. Error: {str(e)}", "error")
            settings = None

        return render_template('profile_sub/home_surroundings.html', settings=settings)

    # If the request is POST, handle the form submission (updating settings)
    elif request.method == 'POST':
        # Handle updates here if needed (not required for your current scenario)
        pass

@profile_bp.route('/view_analysis')
def view_analysis():
    return render_template('profile_sub/view_analysis.html')
