from ultralytics import YOLO

model = YOLO('yolov8n.pt')
print("Class 47:", model.names[47]) # apple
print("Total classes:", len(model.names))
