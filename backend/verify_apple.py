import httpx

img_path = r"C:\Users\lenovo\.gemini\antigravity\scratch\material-rebirth-ai\backend\uploads\0_f35c553466324720a2e84e0d755ca47f.webp"

with open(img_path, "rb") as f:
    files = [("files", ("apple.webp", f.read(), "image/webp"))]
    data = {
        "location": "Kochi",
        "quantity": "1",
        "unit": "units"
    }
    resp = httpx.post("http://127.0.0.1:8000/api/materials/analyze", data=data, files=files, timeout=60.0)
    print("Status code:", resp.status_code)
    res = resp.json()
    print("Detected Material:", res.get("material", {}).get("material_type"))
    print("Condition:", res.get("assessment", {}).get("condition"))
    print("Reuse Score:", res.get("assessment", {}).get("reuse_score"))
    print("Recommendation:", res.get("assessment", {}).get("recommendation"))
    print("Reasoning:", res.get("assessment", {}).get("reasoning"))
