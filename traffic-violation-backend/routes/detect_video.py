from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import cv2
import shutil
from collections import deque

from detector import detect
from detector.tracker import track_objects
from detector.rules import check_violations
from detector.tl_state import TrafficLightState
from detector.speed import SpeedEstimator
from utils.io import save_frame
from utils.video_split import save_violation_clip

router = APIRouter()

# initialize helpers
tl_tracker = TrafficLightState()
speed_estimator = SpeedEstimator()

@router.post("/detect-video")
async def detect_video(file: UploadFile = File(...)):
    try:
        print(f"Received video upload: {file.filename}")

        # Save uploaded video
        upload_folder = "./data/uploaded_videos"
        os.makedirs(upload_folder, exist_ok=True)
        video_path = os.path.join(upload_folder, file.filename)

        with open(video_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        print(f"Saved video to {video_path}")

        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return JSONResponse(status_code=400, content={"message": "Could not open video."})

        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        frame_count = 0
        violations = []
        violation_folder = "./data/violations"
        os.makedirs(violation_folder, exist_ok=True)

        # Keep buffer of last ~5 seconds of frames
        buffer_seconds = 5
        frames_buffer = deque(maxlen=fps * buffer_seconds)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frames_buffer.append((frame_count, frame))

            detections = detect.detect_objects(frame)
            tracked_objs = track_objects(frame, detections)
            light_state = tl_tracker.update(detections)

            for obj in tracked_objs:
                speed = speed_estimator.estimate(obj["track_id"], obj["bbox"])
                obj["speed_kph"] = speed

            frame_violations = check_violations(light_state, tracked_objs, detections)

            if frame_violations:
                # Save violation frame
                violation_frame_path = os.path.join(
                    violation_folder, f"violation_{frame_count}.jpg"
                )
                save_frame(frame, violation_frame_path)

                # Save short video clip around violation
                clip_path = save_violation_clip(
                    frames_buffer, violation_frame_index=frame_count, fps=fps, clip_seconds=4, violation_id=frame_count
                )

                violations.append({
                    "frame": frame_count,
                    "image_url": f"/violations/violation_{frame_count}.jpg",
                    "clip_url": f"/violations/clips/violation_{frame_count}_clip.mp4" if clip_path else None,
                    "violations": frame_violations,
                })

            frame_count += 1

        cap.release()
        return {"message": "Video processed", "violations": violations}

    except Exception as e:
        print(f"Exception occurred: {e}")
        return JSONResponse(status_code=500, content={"message": f"Server error: {str(e)}"})
