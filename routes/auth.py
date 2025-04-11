from flask import Blueprint, render_template, request, redirect, url_for, session
import json
import pyrebase

auth_bp = Blueprint('auth_bp', __name__)

# Load Firebase config
with open('fb-nonadmin.json') as f:
    firebase_config = json.load(f)

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        action = request.form.get('action')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            if action == 'login':
                user = auth.sign_in_with_email_and_password(email, password)
                session['user'] = user['email']
                session['user_id'] = user['localId']
                message = "✅ Login successful! Redirecting..."
                return redirect(url_for('live_feed_bp.live_feed'))  # Adjust based on your route
            elif action == 'signup':
                auth.create_user_with_email_and_password(email, password)
                message = "🎉 Signup successful! Please log in."
        except Exception as e:
            message = "❌ Invalid email or password."
            print(e)

    return render_template("login.html", message=message)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_bp.login'))
