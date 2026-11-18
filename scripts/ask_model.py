import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:4b"


def ask(prompt):
    """Send one prompt to the local model and return its answer."""
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,                  # no reasoning text, just the answer
        "options": {"temperature": 0},   # same answer every time
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        answer = json.loads(response.read().decode("utf-8"))
    return answer["message"]["content"].strip()


if __name__ == "__main__":
    prompt = (
        "Translate the following Turkish sentence into English. "
        "Reply with the translation only.\n\n"
        "O bir doktor."
    )
    print(ask(prompt))
