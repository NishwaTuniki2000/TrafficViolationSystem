from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import cv2
import numpy as np
import base64
import os

from routes import detect_video  # your existing router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

# Mount static files at /data
app.mount("/violations", StaticFiles(directory="data/violations"), name="violations")

# Include routes from detect_video.py
app.include_router(detect_video.router)

# Load trained YOLO model
traffic_model = YOLO("models/yolov8_traffic.pt")

# Detection logic
def detect_red_light_violation(frame):
    results = traffic_model(frame)[0]
    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        if conf > 0.5:
            return True
    return False

# Your video upload endpoint
@app.post("/upload-video")
async def upload_video(video: UploadFile = File(...)):
    try:
        contents = await video.read()
        filename = f"./data/uploaded_videos/{video.filename}"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "wb") as f:
            f.write(contents)

        cap = cv2.VideoCapture(filename)
        if not cap.isOpened():
            return JSONResponse(status_code=400, content={"message": "Could not open video."})

        ret, frame = cap.read()
        if not ret:
            return JSONResponse(status_code=400, content={"message": "Failed to read frames."})

        violations = []
        while ret:
            if detect_red_light_violation(frame):
                violations.append("Violation Detected")
            ret, frame = cap.read()

        cap.release()
        return {"message": "Video processed", "violations": violations}

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Server error: {str(e)}"})

# Your websocket endpoint
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
