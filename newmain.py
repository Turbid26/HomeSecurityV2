from flask import Flask, render_template, jsonify, Response, request, redirect, url_for, session

from routes.auth import auth_bp
from routes.live_feed import live_feed_bp
from routes.home_alerts import home_alerts_bp
from routes.upload import upload_bp
from routes.remove_face import remove_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.context_processor
def inject_user():
    return dict(user=session.get('user'))

app.register_blueprint(auth_bp)
app.register_blueprint(live_feed_bp)
app.register_blueprint(home_alerts_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(remove_bp)

if __name__ == '__main__':
    app.run(debug=True)