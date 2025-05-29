# livefeed.py
from flask import Blueprint, render_template, jsonify, session, redirect, url_for, Response
from datetime import datetime
from utils.helpers.lf import gen_frames
from utils.fb_config import firestore_db

live_feed_bp = Blueprint('live_feed_bp', __name__)

@live_feed_bp.route('/live', methods=['GET'])
def live_feed():
    if 'user' not in session:
        return redirect(url_for('auth_bp.login'))
    return render_template('livefeed.html')

@live_feed_bp.route('/video_feed')
def video_feed():
    if 'user' not in session:
        return redirect(url_for('auth_bp.login'))
    user_email = session['user']
    return Response(gen_frames(user_email), mimetype='multipart/x-mixed-replace; boundary=frame')

@live_feed_bp.route('/start_recording', methods=['POST'])
def start_recording():
    if 'user' not in session:
        return jsonify({'status': 'unauthorized'}), 401
    user_email = session['user']
    from utils.helpers.lf import recording_flags
    recording_flags[user_email] = True
    print(f"[DEBUG] Recording started for {user_email}")
    return jsonify({'status': 'recording started'})

@live_feed_bp.route('/stop_recording', methods=['POST'])
def stop_recording():
    user_email = session.get('user')
    if not user_email:
        return jsonify({'status': 'unauthorized'}), 401

    from utils.helpers.lf import stop_recording_for_user

    print(f"[DEBUG] Recording stopped for {user_email}")
    try:
        uploaded_url = stop_recording_for_user(user_email)
        if uploaded_url:
            print(f"[DEBUG] Video uploaded to: {uploaded_url}")
        else:
            print(f"[DEBUG] No video uploaded for {user_email}")
        return jsonify({'status': 'recording stopped'})
    except Exception as e:
        print(f"[ERROR] Exception while stopping recording: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500