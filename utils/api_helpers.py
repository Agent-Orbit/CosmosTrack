import os
from dotenv import load_dotenv

def get_api():

    load_dotenv()  

    NASA_API_KEY = os.getenv("NASA_API_KEY")
    return NASA_API_KEY