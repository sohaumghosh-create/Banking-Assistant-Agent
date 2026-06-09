import os

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

if not API_KEY:
    raise ValueError("ERROR: 'GEMINI_API_KEY' environment variable not set. Please set it before running main.py.")