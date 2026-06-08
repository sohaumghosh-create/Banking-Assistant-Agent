import json
import os
import urllib.request
import urllib.error

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

if not API_KEY:
    raise ValueError("ERROR: 'GEMINI_API_KEY' environment variable not set. Please set it before running main.py.")

SYSTEM_PROMPT = """
You are a CLI-based Banking Assistant Agent. Your job is to answer user questions by leveraging tools.
The user account ID is "12345".

Available Tools:
1. get_account_balance(account_id) -> Returns {"savings": X, "current": Y}
2. get_recent_transactions(account_id, count=10) -> Returns a list of transactions
3. get_upcoming_payments(account_id) -> Returns upcoming EMIs and bills

You must analyze the user query and decide your plan. Output your response in exactly one of the two following JSON structures. Do not wrap it in markdown block tags like ```json.

Format 1: If you need to fetch information using a tool, output:
{"status": "call_tool", "tool_name": "name_of_the_tool", "arguments": {"account_id": "12345"}}

Format 2: If you have gathered all necessary information to completely answer the user, output:
{"status": "final_answer", "answer": "Your human-friendly final response text with clear breakdowns here."}
"""

def call_gemini(messages: list) -> dict:
    """Sends conversational history to the Gemini API via raw urllib and extracts the decision JSON."""
    payload = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": messages,
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers = {
            "x-goog-api-key": API_KEY,
            "Content-Type": "application/json",
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            raw_text = res_json['candidates'][0]['content']['parts'][0]['text']
            return json.loads(raw_text.strip())
    except urllib.error.HTTPError as e:
        print(f"\n[API Error]: Check your API key. Details: {e.read().decode('utf-8')}")
        raise e