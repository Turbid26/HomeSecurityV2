from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from firebase_admin import db

live_feed_bp = Blueprint('live_feed_bp', __name__)

@live_feed_bp.route('/live', methods=['GET'])
def live_feed():
    if 'user' not in session:
        return redirect(url_for('auth_bp.login'))
    return render_template('livefeed.html')

@live_feed_bp.route('/live_data', methods=['GET'])
def live_data():
    try:
        ref = db.reference("sensorData")
        data = ref.get()
        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "No data available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
