from ultralytics import YOLO
import cv2

# Load the trained model
model = YOLO("models/yolov8_traffic.pt")  # relative path

# Get class names
class_names = model.names  # {class_id: class_name}

def detect_objects(frame, conf_thresh=0.25):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run detection
    results = model.predict(rgb_frame, imgsz=640, conf=conf_thresh)[0]

    detections = []
    for box in results.boxes:
        conf = float(box.conf[0].item())
        if conf < conf_thresh:
            continue

        cls_id = int(box.cls[0].item())
        class_name = class_names.get(cls_id, "unknown")
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

        detections.append({
            "class_id": cls_id,
            "class_name": class_name,
            "confidence": conf,
            "bbox": [x1, y1, x2, y2]
        })

    return detections
