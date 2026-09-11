import httpx

img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\db35918a-fa81-40a7-8c68-7717e5e6c206\media__1789104724446.jpg"

with open(img_path, "rb") as f:
    files = [("files", ("broken_brick.jpg", f.read(), "image/jpeg"))]
    data = {
        "material_type": "brick",
        "location": "Kochi",
        "quantity": "500",
        "unit": "units"
    }
    
    resp = httpx.post("http://127.0.0.1:8000/api/materials/analyze", data=data, files=files, timeout=60.0)
    print("Status:", resp.status_code)
    res_json = resp.json()
    print("Condition:", res_json.get("assessment", {}).get("condition"))
    print("Reuse Score:", res_json.get("assessment", {}).get("reuse_score"))
    print("Defects:", res_json.get("assessment", {}).get("visible_defects"))
    print("Recommendation:", res_json.get("assessment", {}).get("recommendation"))
