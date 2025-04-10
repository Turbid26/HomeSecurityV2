from flask import Flask, render_template, jsonify, Response, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, db
import pyrebase
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize Firebase
def initialize_firebase():
    cred = credentials.Certificate("fb-admin.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ard-cloud-test-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

with open('fb-nonadmin.json') as f:
    firebaseConfig = json.load(f)

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

if not firebase_admin._apps:
    initialize_firebase()

def get_db_reference():
    """Returns Firebase database reference"""
    return db.reference()

@app.route('/',  methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        action = request.form['action']
        email = request.form['email']
        password = request.form['password']
        try:
            if action == 'login':
                user = auth.sign_in_with_email_and_password(email, password)
                message = "✅ Login successful! Please Wait....."
                session['user'] = user['email']
                return redirect(url_for('live_feed'))
            elif action == 'signup':
                auth.create_user_with_email_and_password(email, password)
                message = "🎉 User created successfully!"
        except:
            message = "❌ Error: Invalid email or password."
    return render_template("login.html", message=message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.context_processor
def inject_user():
    return dict(user=session.get('user'))

@app.route('/live', methods=['GET', 'POST'])
def live_feed():
    return render_template('livefeed.html')

@app.route('/live_data')
def live_data():
    ref = db.reference("sensorData")
    data = ref.get()

    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "No data available"}), 404

@app.route('/home_alerts')
def home_alerts():
    return render_template('homealerts.html')

@app.route('/alerts_data')
def alerts_data():
    ref = db.reference("sensorData")
    data = ref.get()

    if data:
        return jsonify({
            "motion": data.get("motion", 0),
            "temperature": data.get("temperature", 0)
        })
    else:
        return jsonify({"error": "No data available"}), 404

@app.route('/get_alerts')
def get_alerts():
    ref = get_db_reference().child("alerts")
    alerts = ref.get()  # Fetch alerts from Firebase
    
    if alerts:
        alerts_list = [{"type": v["type"], "message": v["message"], "timestamp": v["timestamp"]} for k, v in alerts.items()]
        return jsonify(alerts_list)
    
    return jsonify([])  # Return empty list if no alerts


if __name__ == '__main__':
    app.run(debug=True)
