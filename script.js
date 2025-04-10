// // Firebase config (same as in your Python script)
// const firebaseConfig = {
//     apiKey: "AIzaSyCyBRyTL_d_cz1Bbu9sL3NUTEhqUITXIus",
//     authDomain: "pythonloginauth-9505f.firebaseapp.com",
//     projectId: "pythonloginauth-9505f",
//     databaseURL: "https://pythonloginauth-9505f-default-rtdb.firebaseio.com",
//     storageBucket: "pythonloginauth-9505f.appspot.com",
//     messagingSenderId: "677967221518",
//     appId: "1:677967221518:web:0b1b648f9aefb9c7b9bd5f"
//   };
  
//   firebase.initializeApp(firebaseConfig);
//   const auth = firebase.auth();
  
//   let isLogin = true;
  
//   function toggleForm() {
//     isLogin = !isLogin;
//     document.getElementById("form-title").textContent = isLogin ? "Login" : "Sign Up";
//     document.querySelector("button").textContent = isLogin ? "Login" : "Sign Up";
//     document.getElementById("toggle-text").innerHTML = isLogin
//       ? `New user? <a onclick="toggleForm()">Sign up here</a>`
//       : `Already have an account? <a onclick="toggleForm()">Login here</a>`;
//     document.getElementById("message").textContent = "";
//   }
  
//   function handleAuth() {
//     const email = document.getElementById("email").value;
//     const password = document.getElementById("password").value;
//     const message = document.getElementById("message");
  
//     if (!email || !password) {
//       message.textContent = "Please fill out all fields.";
//       return;
//     }
  
//     if (isLogin) {
//       auth.signInWithEmailAndPassword(email, password)
//         .then(user => {
//           message.style.color = "green";
//           message.textContent = "Login successful!";
//         })
//         .catch(err => {
//           message.textContent = "Invalid email or password.";
//         });
//     } else {
//       auth.createUserWithEmailAndPassword(email, password)
//         .then(user => {
//           message.style.color = "green";
//           message.textContent = "User created successfully!";
//         })
//         .catch(err => {
//           message.textContent = "Email already exists or password is weak.";
//         });
//     }
//   }
  