import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:4b"   # must match the name in `ollama list`


def ask(prompt):
    """Send one prompt to the local model and return its answer."""
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,
        "options": {"temperature": 0},
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        answer = json.loads(response.read().decode("utf-8"))
    text = answer["message"]["content"]
    if "</think>" in text:              # safety net: drop any reasoning text
        text = text.split("</think>")[-1]
    return text.strip()


if __name__ == "__main__":
    prompt = (
        "Translate the following Turkish sentence into English. "
        "Reply with the translation only.\n\n"
        "O bir doktor."
    )
    print(ask(prompt))
