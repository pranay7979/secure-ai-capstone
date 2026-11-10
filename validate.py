
import re
import base64


MAX_INPUT_LENGTH = 500

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+all\s+instructions",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"show\s+(me\s+)?(the\s+)?system\s+prompt",
    r"you\s+are\s+now",
    r"jailbreak",
    r"act\s+as\s+if",
    r"bypass\s+(the\s+)?(security|restrictions|rules)"
]


def validate_input(user_input):

    if not isinstance(user_input, str) or not user_input.strip():
        return False, "Message cannot be empty"

    if len(user_input) > MAX_INPUT_LENGTH:
        return False, "Message exceeds maximum allowed length"

    text = user_input.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False, "Potential prompt injection detected"

    # Check for Base64-encoded instructions
    encoded_pattern = r"[A-Za-z0-9+/]{20,}={0,2}"

    for match in re.findall(encoded_pattern, user_input):
        try:
            decoded = base64.b64decode(
                match,
                validate=True
            ).decode("utf-8", errors="ignore")

            decoded_lower = decoded.lower()

            for pattern in INJECTION_PATTERNS:
                if re.search(pattern, decoded_lower, re.IGNORECASE):
                    return False, "Encoded prompt injection detected"

        except Exception:
            continue

    return True, "Input accepted"

