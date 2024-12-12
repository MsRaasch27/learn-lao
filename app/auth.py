import os
import urllib.parse
from fastapi.responses import RedirectResponse
import requests
from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import firestore
from fastapi.security import OAuth2PasswordBearer
from firebase_admin.auth import verify_id_token
from app.database import db
from dotenv import load_dotenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

# Load environment variables
load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

@router.get("/google-login")
def google_login():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
    }
    url = f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)

@router.get("/google/callback")
def google_callback(code: str):
    try:
        # Exchange the authorization code for an access token
        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = requests.post(GOOGLE_TOKEN_URL, data=data)
        response.raise_for_status()
        token_info = response.json()
        google_id_token = token_info.get("id_token")

        if not google_id_token:
            raise HTTPException(status_code=400, detail="Missing Google access token")
        
        print("Google Access Token:", google_id_token)

        # Exchange the Google access token for a Firebase ID token
        firebase_id_token = exchange_google_token_for_firebase_token(google_id_token)

        # Verify the Firebase ID token and proceed
        decoded_token = verify_id_token(firebase_id_token, clock_skew_seconds=5)
        user_email = decoded_token.get("email")
        user_firstName = decoded_token.get("given_name")

        # Add user to Firestore if not exists
        user_ref = db.collection("users").document(user_email)
        if not user_ref.get().exists:
            user_ref.set({
                "email": user_email,
                "firstName": user_firstName,
            })
            return {"message": "User created successfully", "email": user_email}
        else:
            return {"message": "User already exists", "email": user_email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during authentication: {e}")

@router.get("/google")
def authenticate_user(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = verify_id_token(token)
        user_email = decoded_token.get("email")
        user_firstName = decoded_token.get("firstName")

        #Add user to Firestore if not exists
        user_ref = db.collection("users").document(user_email)
        if not user_ref.get().exists:
            user_ref.set({
                "email": user_email,
                "firstName": user_firstName,
            })
            return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def exchange_google_token_for_firebase_token(google_id_token: str) -> str:
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={FIREBASE_API_KEY}"
    payload = {
        "postBody": f"id_token={google_id_token}&providerId=google.com",
        "requestUri": "http://localhost",  # This can be any valid URL
        "returnIdpCredential": True,
        "returnSecureToken": True,
    }
    response = requests.post(url, json=payload)
    print("Payload:", payload)
    print("Response status code:", response.status_code)
    print("Response content:", response.content.decode())
    response.raise_for_status()
    firebase_token_info = response.json()
    return firebase_token_info["idToken"]
