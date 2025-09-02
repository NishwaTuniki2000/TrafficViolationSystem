from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np
import base64
from ultralytics import YOLO

from routes import detect_video  # upload handler from detect_video.py

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can replace "*" with your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve violation images & clips
app.mount("/violations", StaticFiles(directory="data/violations"), name="violations")

# Include /detect-video route from detect_video.py
app.include_router(detect_video.router)

def detect_red_light_violation(frame):
    # Load YOLOv8n on demand (smallest model, ~5MB)
    model = YOLO("yolov8n.pt")
    results = model(frame)[0]
    for box in results.boxes:
        conf = float(box.conf[0])
        if conf > 0.5:
            return True
    return False


# Live video WebSocket endpoint
@app.websocket("/live-video")
async def live_video(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            frame_data = await websocket.receive_text()
            img_data = base64.b64decode(frame_data.split(",")[1])
            np_frame = np.frombuffer(img_data, dtype=np.uint8)
            img = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)

            if detect_red_light_violation(img):
                await websocket.send_text("Violation detected")
            else:
                await websocket.send_text("No violation")
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
