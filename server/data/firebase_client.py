import firebase_admin
from firebase_admin import credentials, firestore
import os

cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), "../utils/firebase_cred.json"))

firebase_admin.initialize_app(cred)
db = firestore.client()