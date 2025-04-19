from utils.fb_config import firestore_db

user_email = 'a@gmail.com'

face_entry = {"timestamp" : "2025-04-19T12:45:00",
"image_url" : "https://res.cloudinary.com/duhho2j3z/image/upload/v1744966707/HomeSec/Known/test_1744946906.jpg",
"label" : "test"
}

user_ref = firestore_db.collection("users").document(user_email)
user_doc = user_ref.get()
faces = user_doc.to_dict().get("alerted_faces", [])
faces.append(face_entry)
user_ref.update({
                    "alerted_faces": faces
                })