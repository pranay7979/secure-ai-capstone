
import os
import jwt
from functools import wraps
from flask import request, jsonify


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # Read JWT from Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({
                "error": "Authorization token is missing"
            }), 401

        token = auth_header.split(" ", 1)[1].strip()

        if not token:
            return jsonify({
                "error": "Authorization token is missing"
            }), 401

        # Load secret from environment variable
        secret = os.getenv("JWT_SECRET")

        if not secret:
            return jsonify({
                "error": "Authentication configuration error"
            }), 500

        try:
            # Verify JWT signature and expiration
            payload = jwt.decode(
                token,
                secret,
                algorithms=["HS256"]
            )

            request.user = payload

        except jwt.ExpiredSignatureError:
            return jsonify({
                "error": "Token has expired"
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                "error": "Invalid token"
            }), 401

        return f(*args, **kwargs)

    return decorated

