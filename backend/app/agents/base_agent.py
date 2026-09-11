import json
import httpx
from typing import Optional
from app.config import get_settings


class BaseAgent:
    """Base class for all AI agents with LLM integration and mock fallback."""

    def __init__(self):
        self.settings = get_settings()
        self._has_llm = bool(self.settings.GROQ_API_KEY)

    @property
    def is_demo_mode(self) -> bool:
        return self.settings.DEMO_MODE or not self._has_llm

    def llm_call(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Call the LLM. Returns None if no API key."""
        if not self._has_llm:
            return None
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(
                    f"{self.settings.LLAMA_BASE_URL}/chat/completions",
                    headers={"Authorization": f"Bearer {self.settings.GROQ_API_KEY}",
                             "Content-Type": "application/json"},
                    json={"model": self.settings.LLAMA_MODEL, "messages": messages,
                          "temperature": 0.3, "max_tokens": 2000}
                )
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"]
        except Exception:
            return None

    def llm_call_vision(self, prompt: str, image_paths: list[str], system_prompt: str = "") -> Optional[str]:
        """Call the LLM with images using a vision model."""
        if not self._has_llm:
            return None
        import base64
        import mimetypes
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            content = [{"type": "text", "text": prompt}]
            for path in image_paths:
                try:
                    import os
                    filename = os.path.basename(path)
                    real_path = os.path.join(self.settings.UPLOAD_DIR, filename)
                    with open(real_path, "rb") as image_file:
                        b64 = base64.b64encode(image_file.read()).decode("utf-8")
                        mime = mimetypes.guess_type(real_path)[0] or "image/jpeg"
                        content.append({
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime};base64,{b64}"}
                        })
                except Exception as e:
                    print("Error loading image for vision:", e)
                    continue
            
            messages.append({"role": "user", "content": content})
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(
                    f"{self.settings.LLAMA_BASE_URL}/chat/completions",
                    headers={"Authorization": f"Bearer {self.settings.GROQ_API_KEY}",
                             "Content-Type": "application/json"},
                    json={"model": getattr(self.settings, 'LLAMA_VISION_MODEL', 'llama-3.2-11b-vision-preview'), "messages": messages,
                          "temperature": 0.3, "max_tokens": 2000}
                )
                if resp.status_code != 200:
                    print("Groq Vision API Error details:", resp.text)
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print("Vision API Error:", e)
            return None

    def parse_json_response(self, text: str) -> Optional[dict]:
        if not text:
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            try:
                start = text.index('{')
                end = text.rindex('}') + 1
                return json.loads(text[start:end])
            except (ValueError, json.JSONDecodeError):
                return None
