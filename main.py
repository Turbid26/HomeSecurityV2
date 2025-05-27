import threading

from flask import Flask, session

from routes.auth import auth_bp
from routes.live_feed import live_feed_bp
from routes.home_alerts import home_alerts_bp
from routes.upload import upload_bp
from routes.remove_face import remove_bp
from routes.profile import profile_bp
from routes.activities import activities_bp

from utils.helpers.alert_monitor import monitor_sensor_data

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
app.register_blueprint(profile_bp)
app.register_blueprint(activities_bp)

if __name__ == '__main__':
    threading.Thread(target=monitor_sensor_data, daemon=True).start()
    app.run(debug=True)