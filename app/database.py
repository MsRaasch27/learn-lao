import os
import json
from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app

load_dotenv()

# JSON in .env file isn't working great
# #FIREBASE_CONFIG = os.getenv("FIREBASE_CONFIG")
# STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

path = "learn-lao-8394d-firebase-adminsdk-w7adf-6f97d34e38.json"
print("File exists:", os.path.exists(path))
cred = credentials.Certificate(path)
firebase_app = initialize_app(cred)
db = firestore.client()


