def check_violations(tl_state, tracked_objs, detections, speed_limit_kph=40):
    violations = []

    for obj in tracked_objs:
        tid = obj["track_id"]
        bbox = obj["bbox"]

        # Example: red light movement
        if tl_state == "red":
            violations.append({"track_id": tid, "type": "Red Light Violation", "bbox": bbox})

        # You can add "no turn on red" and speed check logic here

    return violations
