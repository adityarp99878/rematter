import os
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

resp = httpx.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)

models = resp.json().get("data", [])
for m in models:
    print(m["id"])
