import os


def get_api_url() -> str:
    return os.getenv("API_URL", "http://localhost:8000")
