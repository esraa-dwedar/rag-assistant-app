import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def query_rag_api(question: str):
    url = f"{API_BASE_URL.rstrip('/')}/query"
    try:
        response = requests.post(url, json={"question": question}, timeout=60)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, f"Failed to contact RAG Backend: {str(e)}"

def check_backend_health():
    url = f"{API_BASE_URL.rstrip('/')}/health"
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except:
        return False