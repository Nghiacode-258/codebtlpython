import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyCxms2ug17qh4GwP5qq0fgBTBfhvLOWLQ8",
  'authDomain': "kawaii-f2f0c.firebaseapp.com",
  'databaseURL': "https://kawaii-f2f0c-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "kawaii-f2f0c",
  'storageBucket': "kawaii-f2f0c.firebasestorage.app",
  'messagingSenderId': "1014671314187",
  'appId': "1:1014671314187:web:2c62b562d17f68b5ed660e",
  'measurementId': "G-7Z43834BQR"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()