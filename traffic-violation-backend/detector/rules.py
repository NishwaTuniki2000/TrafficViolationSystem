from detector.speed import SpeedEstimator

# initialize global speed estimator
speed_estimator = SpeedEstimator(pixels_per_meter=8)

def check_violations(tl_state, tracked_objs, detections, speed_limit_kph=40):
    violations = []

    for obj in tracked_objs:
        tid = obj["track_id"]
        bbox = obj["bbox"]

        # Rule 1: Red light violation
        if tl_state == "red":
            violations.append({
                "track_id": tid,
                "type": "Red Light Violation",
                "bbox": bbox
            })

        # Rule 2: Speeding violation
        speed = speed_estimator.estimate(tid, bbox)
        if speed > speed_limit_kph:
            violations.append({
                "track_id": tid,
                "type": f"Overspeeding ({speed:.1f} kph)",
                "bbox": bbox
            })

    return violations
