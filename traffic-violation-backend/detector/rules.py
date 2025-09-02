def check_violations(tl_state, tracked_objs, detections, speed_limit_kph=40):
    violations = []

    for obj in tracked_objs:
        tid = obj["track_id"]
        bbox = obj["bbox"]
        speed = obj.get("speed", None)  # assume tracker attaches speed if available

        # 1. Red light violation (moving while red)
        if tl_state == "red" and obj.get("moving", False):
            violations.append({
                "track_id": tid,
                "type": "Red Light Violation",
                "bbox": bbox
            })

        # 2. Speeding
        if speed and speed > speed_limit_kph:
            violations.append({
                "track_id": tid,
                "type": f"Overspeeding ({speed:.1f} > {speed_limit_kph} kph)",
                "bbox": bbox
            })

        # 3. No Turn on Red (example rule)
        if tl_state == "red" and obj.get("direction") == "left":
            violations.append({
                "track_id": tid,
                "type": "Illegal Left Turn on Red",
                "bbox": bbox
            })

    return violations
