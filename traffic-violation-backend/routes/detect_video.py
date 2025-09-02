from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import cv2
import shutil
from detector import detect

router = APIRouter()

@router.post("/detect-video")
async def detect_video(file: UploadFile = File(...)):
    try:
        print(f"Received video upload: {file.filename}")
        
        # Save uploaded video to data/uploaded_videos/
        upload_folder = "./data/uploaded_videos"
        os.makedirs(upload_folder, exist_ok=True)
        video_path = os.path.join(upload_folder, file.filename)

        with open(video_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        print(f"Saved video to {video_path}")

        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Failed to open video")
            return JSONResponse(status_code=400, content={"message": "Could not open video."})

        frame_count = 0
        violations = []

        # Make sure violations folder exists
        violation_folder = "./data/violations"
        os.makedirs(violation_folder, exist_ok=True)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("No more frames to read.")
                break

            print(f"Processing frame {frame_count}")
            detections = detect.detect_objects(frame)

            if len(detections) > 0:
                violation_frame_path = os.path.join(violation_folder, f"violation_{frame_count}.jpg")
                cv2.imwrite(violation_frame_path, frame)
                print(f"Violation detected on frame {frame_count}, saved image to {violation_frame_path}")

                # return URL that frontend can directly access
                public_url = f"/violations/violation_{frame_count}.jpg"

                violations.append({
                    "frame": frame_count,
                    "image_url": public_url,   # matches FastAPI StaticFiles
                    "detections": detections,
                })

            frame_count += 1

        cap.release()
        print(f"Video processing complete. Total frames processed: {frame_count}")
        print(f"Total violations detected: {len(violations)}")

        return {"message": "Video processed", "violations": violations}

    except Exception as e:
        print(f"Exception occurred: {e}")
        return JSONResponse(status_code=500, content={"message": f"Server error: {str(e)}"})
