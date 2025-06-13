import requests
from dotenv import load_dotenv
import os

load_dotenv()

BACKEND_BASE_URL = os.getenv("http://localhost:8000/api/v1")

def get_tasks_by_project(project_id: str) -> list:
    URL = f"{BACKEND_BASE_URL}/tasks/{project_id}"
    try:
        response = requests.get(URL, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️  Failed to fetch tasks. Status code: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"❌ Error connecting to backend: {e}")
        return []