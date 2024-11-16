import firebase_admin
from firebase_admin import credentials

# Check if Firebase is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate('gym-app-minor-project-da12df6a9c60.json')
    firebase_admin.initialize_app(cred)
