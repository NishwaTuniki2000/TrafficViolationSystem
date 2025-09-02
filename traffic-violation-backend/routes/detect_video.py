from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import cv2
import shutil

from detector import detect
from detector.tracker import track_objects
from detector.rules import check_violations
from detector.tl_state import TrafficLightState
from detector.speed import SpeedEstimator

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

        frame_count = 0
        violations = []
        violation_folder = "./data/violations"
        os.makedirs(violation_folder, exist_ok=True)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            print(f"Processing frame {frame_count}")

            # Step 1: Detect objects
            detections = detect.detect_objects(frame)

            # Step 2: Track objects across frames
            tracked_objs = track_objects(frame, detections)

            # Step 3: Update traffic light state
            light_state = tl_tracker.update(detections)

            # Step 4: Estimate speed for each tracked object
            for obj in tracked_objs:
                speed = speed_estimator.estimate(obj["track_id"], obj["bbox"])
                obj["speed_kph"] = speed

            # Step 5: Check rules (red light, speeding, etc.)
            frame_violations = check_violations(light_state, tracked_objs, detections)

            if frame_violations:
                # Save violation frame
                violation_frame_path = os.path.join(
                    violation_folder, f"violation_{frame_count}.jpg"
                )
                cv2.imwrite(violation_frame_path, frame)

                # Append violations with frame info
                violations.append({
                    "frame": frame_count,
                    "image_url": f"/violations/violation_{frame_count}.jpg",
                    "violations": frame_violations,
                })

            frame_count += 1

        cap.release()
        return {"message": "Video processed", "violations": violations}

    except Exception as e:
        print(f"Exception occurred: {e}")
        return JSONResponse(status_code=500, content={"message": f"Server error: {str(e)}"})
