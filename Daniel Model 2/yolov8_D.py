from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO('yolov8n.pt')  # 'yolov8s.pt' or larger models like 'yolov8l.pt' might be better (ask group)

# Train
model.train(data= "dataset.yaml", epochs=100, imgsz=640)
