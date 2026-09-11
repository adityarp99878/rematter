import os
import base64
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\db35918a-fa81-40a7-8c68-7717e5e6c206\media__1789104724446.jpg"

with open(img_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "model": "llama-3.2-11b-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this image?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
            ]
        }
    ],
    "temperature": 0.3
}

resp = httpx.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json=payload,
    timeout=60.0
)

print(resp.status_code)
print(resp.text)
