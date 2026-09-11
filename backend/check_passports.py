import httpx

resp = httpx.get("http://127.0.0.1:8000/api/materials/")
print("Materials count:", len(resp.json().get("materials", [])))
for m in resp.json().get("materials", []):
    print(f"ID: {m['id']}, Type: {m['material_type']}, Status: {m['status']}")
    p_resp = httpx.get(f"http://127.0.0.1:8000/api/materials/{m['id']}/passport")
    print(f"  Passport status: {p_resp.status_code}")
