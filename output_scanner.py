
import re


SYSTEM_PROMPT_MARKERS = [
    "system prompt:",
    "you are a helpful assistant",
    "system instructions:",
    "confidential system instructions"
]

CREDENTIAL_PATTERN = re.compile(
    r"(sk-[A-Za-z0-9_-]{12,}|"
    r"api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_-]{12,})",
    re.IGNORECASE
)


def scan_output(response):

    if not isinstance(response, str):
        return False, "Unsafe response blocked"

    text = response.lower()

    for marker in SYSTEM_PROMPT_MARKERS:
        if marker in text:
            return False, "Unsafe response blocked"

    if CREDENTIAL_PATTERN.search(response):
        return False, "Unsafe response blocked"

    return True, response

