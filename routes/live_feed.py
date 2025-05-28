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
