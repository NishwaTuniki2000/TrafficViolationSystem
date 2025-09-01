from ultralytics import YOLO
import cv2

# Load the trained model
model = YOLO("models/yolov8_traffic.pt")  # make sure this path is correct

# Get class names from model
class_names = model.names  # {class_id: class_name}

def detect_objects(frame, conf_thresh=0.3):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = model(rgb_frame)[0]  # YOLOv8 returns a list; we use the first element

    detections = []
    for box in results.boxes:
        conf = float(box.conf)
        if conf < conf_thresh:
            continue

        cls_id = int(box.cls)
        class_name = class_names.get(cls_id, "unknown")
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        detections.append({
            "class_id": cls_id,
            "class_name": class_name,
            "confidence": conf,
            "bbox": [x1, y1, x2, y2]
        })

    return detections
