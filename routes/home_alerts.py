from flask import Blueprint, render_template, jsonify, session
from firebase_admin import db
from utils.fb_config import get_realtime_db 

home_alerts_bp = Blueprint('home_alerts_bp', __name__, template_folder='../templates')

@home_alerts_bp.route('/home_alerts')
def home_alerts():
    return render_template('home_alerts.html')

@home_alerts_bp.route('/get_alerts')
def get_alerts():
    user_id = session.get('user_id')
    print(user_id)
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    ref = get_realtime_db().child("alerts").child(user_id)
    alerts = ref.get()

    if alerts:
        alerts_list = [
            {
                "type": alert.get("type", "unknown"),
                "message": alert.get("message", "No message"),
                "timestamp": alert.get("timestamp", "Unknown time")
            }
            for alert in alerts.values()
        ]
        return jsonify(alerts_list)

    return jsonify([])
