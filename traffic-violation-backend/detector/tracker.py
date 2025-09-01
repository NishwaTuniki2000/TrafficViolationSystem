from deep_sort_realtime.deepsort_tracker import DeepSort

tracker = DeepSort(max_age=5)

def track_objects(frame, detections):
    input_dets = [
        [*d["bbox"], d["confidence"], str(d["class_id"])] for d in detections
    ]
    tracks = tracker.update_tracks(input_dets, frame=frame)
    tracked = []
    for t in tracks:
        if not t.is_confirmed():
            continue
        track_id = t.track_id
        ltrb = t.to_ltrb()
        tracked.append({"track_id": track_id, "bbox": ltrb})
    return tracked
