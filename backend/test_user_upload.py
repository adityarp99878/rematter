from ultralytics import YOLO

model = YOLO('yolov8n.pt')
results = model(r"C:\Users\lenovo\.gemini\antigravity\scratch\material-rebirth-ai\backend\uploads\0_f35c553466324720a2e84e0d755ca47f.webp")
for r in results:
    for box in r.boxes:
        cls_id = int(box.cls[0].item())
        name = model.names[cls_id]
        conf = float(box.conf[0].item())
        print(f"Detected: {name} ({conf:.2f})")
