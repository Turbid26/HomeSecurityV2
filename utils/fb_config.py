import firebase_admin
from firebase_admin import credentials, firestore, db as realtime_db

cred = credentials.Certificate("fb-admin.json")
firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ard-cloud-test-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

firestore_db = firestore.client()

def get_realtime_db():
    return realtime_db.reference()
