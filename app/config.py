import os

class Config:
    FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")