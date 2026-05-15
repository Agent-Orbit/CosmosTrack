import os
from dotenv import load_dotenv
import json

def get_api():

    load_dotenv()  

    NASA_API_KEY = os.getenv("NASA_API_KEY")
    return NASA_API_KEY

FAVORITES_FILE = "database/favorites.json"

def load_favorites():
    
    os.makedirs("database", exist_ok=True)
    
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_favorites(favorites):
    
    os.makedirs("database", exist_ok=True)
    
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=2)