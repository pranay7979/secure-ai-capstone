
import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

secret = os.getenv("JWT_SECRET")

if not secret:
    raise RuntimeError("JWT_SECRET is not configured")

payload = {
    "sub": "capstone-user",
    "exp": datetime.now(timezone.utc) + timedelta(hours=1)
}

token = jwt.encode(payload, secret, algorithm="HS256")

print("Generated JWT:")
print(token)

