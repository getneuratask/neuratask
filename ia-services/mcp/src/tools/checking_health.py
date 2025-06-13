import requests
from dotenv import load_dotenv
import os


load_dotenv()
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")


def check_health() -> bool:
    URL= BACKEND_BASE_URL + "/health"
    try:
        response = requests.get(URL, timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy.")
        else:
            print(f"⚠️  Backend health check failed. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Error connecting to backend: {e}")
