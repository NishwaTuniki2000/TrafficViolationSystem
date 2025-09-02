from detector.speed import SpeedEstimator

# global speed estimator instance
speed_estimator = SpeedEstimator(pixels_per_meter=8)

def check_violations(tl_state, tracked_objs, detections, speed_limit_kph=40):
    """
    Check violations: red-light and overspeeding.
    tl_state: traffic light state ("red" / "green")
    tracked_objs: list of {track_id, bbox}
    detections: output from YOLO (not heavily used here yet)
    """
    violations = []

    for obj in tracked_objs:
        tid = obj["track_id"]
        bbox = obj["bbox"]

        # Rule 1: Red Light Violation
        if tl_state == "red":
            violations.append({
                "track_id": tid,
                "type": "Red Light Violation",
                "bbox": bbox
            })

        # Rule 2: Overspeeding
        speed = speed_estimator.estimate(tid, bbox)
        if speed > speed_limit_kph:
            violations.append({
                "track_id": tid,
                "type": f"Overspeeding ({speed:.1f} kph)",
                "bbox": bbox
            })

    return violations
