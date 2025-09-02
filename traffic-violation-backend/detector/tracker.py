from deep_sort_realtime.deepsort_tracker import DeepSort

# Initialize DeepSORT tracker
tracker = DeepSort(
    max_age=5,          # how many frames to keep "lost" tracks before deletion
    n_init=2,           # how many detections before confirming a track
    max_cosine_distance=0.3,
    nms_max_overlap=1.0,
)

def track_objects(frame, detections):
    """
    Run DeepSORT tracking on YOLO detections.
    Args:
        frame (numpy.ndarray): current video frame (BGR).
        detections (list): YOLO detections, each like:
            { "class_id": int, "class_name": str, "confidence": float, "bbox": [x1, y1, x2, y2] }
    Returns:
        list of dicts: tracked objects with unique IDs:
            { "track_id": int, "bbox": [l, t, r, b], "class_id": int, "class_name": str }
    """
    # Prepare detections in DeepSORT format [x1, y1, x2, y2, conf, class]
    input_dets = [
        [*d["bbox"], d["confidence"], str(d["class_id"])]
        for d in detections
    ]

    # Update DeepSORT
    tracks = tracker.update_tracks(input_dets, frame=frame)

    tracked = []
    for t in tracks:
        if not t.is_confirmed():
            continue
        l, t_, r, b = t.to_ltrb()
        tracked.append({
            "track_id": t.track_id,
            "bbox": [int(l), int(t_), int(r), int(b)],
            "class_id": int(t.get_det_class()),  # from YOLO class
            "class_name": t.get_det_class(),     # stored as str
        })

    return tracked
