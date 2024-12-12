# Set up virtual environment
python3.9 -m venv myenv
source myenv/bin/activate

# Create project structure
touch requirements.txt
touch .env
touch Dockerfile
touch .gitignore
mkdir app
touch app/__init__.py app/main.py app/auth.py app/payment.py app/models.py app/database.py
mkdir app/routes app/templates
touch app/routes/__init__.py app/routes/content.py
pip install -r requirements.txt (did the weird thing where it wanted to make a venv again, just did it with the default Python interpreter)
Start Docker Desktop
docker build -t fastapi-app .
docker run -p 8080:8080 fastapi-app

To run without having to build: docker run -p 8080:8080 -v $(pwd):/app fastapi-app

##
Navigate to http://localhost:8080/auth/google-login

# App Functionality
- Main.py serves as the entry point for the FastAPI application
- Reroutes to auth.py where the google-login route allows user to sign in with their Google account and then redirects to the callback route.
Google credentials can be obtained from the Google Cloud Console.
- firebase_app = initialize_app(cred) weirdly uses the credentials from the .env file instead of what's passed to it.
- *