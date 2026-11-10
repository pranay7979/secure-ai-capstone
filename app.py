
import os
import requests

from flask import Flask, request, jsonify
from dotenv import load_dotenv

from auth import token_required
from validate import validate_input
from output_scanner import scan_output

load_dotenv()

app = Flask(__name__)

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/chat"
)

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")


@app.route("/chat", methods=["POST"])
@token_required
def chat():

    # Check request body
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({
            "error": "Message is required"
        }), 400

    user_message = data["message"]

    # Input validation
    is_valid, validation_message = validate_input(user_message)

    if not is_valid:
        return jsonify({
            "error": validation_message
        }), 400

    # Call Ollama only after authentication and validation
    try:
        ollama_response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "stream": False
            },
            timeout=120
        )

        ollama_response.raise_for_status()

        result = ollama_response.json()
        ai_response = result["message"]["content"]

    except requests.exceptions.RequestException:
        return jsonify({
            "error": "AI service is currently unavailable"
        }), 503

    except (ValueError, KeyError, TypeError):
        return jsonify({
            "error": "Invalid response from AI service"
        }), 502

    # Output scanning
    is_safe, scanned_response = scan_output(ai_response)

    if not is_safe:
        return jsonify({
            "error": "AI response blocked by security scanner"
        }), 502

    return jsonify({
        "reply": scanned_response
    }), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )

