# import pyrebase

# firebaseConfig = {
#     'apiKey': "AIzaSyCyBRyTL_d_cz1Bbu9sL3NUTEhqUITXIus",
#     'authDomain': "pythonloginauth-9505f.firebaseapp.com",
#     'projectId': "pythonloginauth-9505f",
#     'databaseURL': "https://pythonloginauth-9505f-default-rtdb.firebaseio.com",
#     'storageBucket': "pythonloginauth-9505f.appspot.com",  # Fixed
#     'messagingSenderId': "677967221518",
#     'appId': "1:677967221518:web:0b1b648f9aefb9c7b9bd5f"
# }

# firebase = pyrebase.initialize_app(firebaseConfig)
# auth = firebase.auth()

# def login():
#     print("Login ...")
#     email = input("Enter email: ")
#     password = input("Enter password: ")
#     try:
#         user = auth.sign_in_with_email_and_password(email, password)
#         print("Login successful!")
#     except:
#         print("Invalid email or password.")

# def signup():
#     print("Sign up ...")
#     email = input("Enter email: ")
#     password = input("Enter password: ")
#     try:
#         user = auth.create_user_with_email_and_password(email, password)
#         print("User created successfully!")
#     except:
#         print("Email already exists or password is weak.")

# ans = input("Are you a new user (y/n)? ")
# if ans.lower() == 'n':
#     login()
# elif ans.lower() == 'y':
#     signup()
# else:
#     print("Invalid input.")
from flask import Flask, render_template, request
import pyrebase

app = Flask(__name__)

# Firebase config
firebaseConfig = {
    'apiKey': "AIzaSyCyBRyTL_d_cz1Bbu9sL3NUTEhqUITXIus",
    'authDomain': "pythonloginauth-9505f.firebaseapp.com",
    'projectId': "pythonloginauth-9505f",
    'databaseURL': "https://pythonloginauth-9505f-default-rtdb.firebaseio.com",
    'storageBucket': "pythonloginauth-9505f.appspot.com",
    'messagingSenderId': "677967221518",
    'appId': "1:677967221518:web:0b1b648f9aefb9c7b9bd5f"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        action = request.form['action']
        email = request.form['email']
        password = request.form['password']
        try:
            if action == 'login':
                auth.sign_in_with_email_and_password(email, password)
                message = "✅ Login successful!"
            elif action == 'signup':
                auth.create_user_with_email_and_password(email, password)
                message = "🎉 User created successfully!"
        except:
            message = "❌ Error: Invalid email or password."
    return render_template("index.html", message=message)

if __name__ == '__main__':
    app.run(debug=True)
