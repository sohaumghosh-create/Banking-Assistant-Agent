import json
import urllib.request
import urllib.error

from config import API_KEY, API_URL
from agent.prompt import SYSTEM_PROMPT

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