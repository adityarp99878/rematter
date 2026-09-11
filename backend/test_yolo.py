from ultralytics import YOLO

# Load standard nano model
model = YOLO('yolov8n.pt')

# Test apple
results = model(r"C:\Users\lenovo\.gemini\antigravity\scratch\material-rebirth-ai\backend\test_apple.jpg")
for r in results:
    for box in r.boxes:
        cls_id = int(box.cls[0].item())
        name = model.names[cls_id]
        conf = float(box.conf[0].item())
        print(f"Detected: {name} ({conf:.2f})")
