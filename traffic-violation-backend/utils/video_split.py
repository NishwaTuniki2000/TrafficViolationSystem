import os
from collections import deque

CLIP_SAVE_PATH = "data/violations/clips"
os.makedirs(CLIP_SAVE_PATH, exist_ok=True)

def save_violation_clip(frames_buffer, violation_frame_index, fps=30, clip_seconds=4, violation_id=0):
    # frames_buffer is a deque of recent frames, with frame indices
    # violation_frame_index is the index of the frame where violation happened

    start_frame = max(0, violation_frame_index - int(fps * (clip_seconds / 2)))
    end_frame = violation_frame_index + int(fps * (clip_seconds / 2))

    # Collect frames in this range from buffer or video source
    # For simplicity, let's assume frames_buffer holds frames in order with frame index
    
    clip_frames = [frame for idx, frame in frames_buffer if start_frame <= idx <= end_frame]

    if not clip_frames:
        print("No frames found for violation clip")
        return None

    clip_path = os.path.join(CLIP_SAVE_PATH, f"violation_{violation_id}_clip.mp4")
    height, width, _ = clip_frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(clip_path, fourcc, fps, (width, height))

    for frame in clip_frames:
        out.write(frame)
    out.release()

    return clip_path
