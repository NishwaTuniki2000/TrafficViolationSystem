# Simple FSM (finite state machine) to track red/green traffic light state

class TrafficLightState:
    def __init__(self):
        self.state = "unknown"

    def update(self, detections):
        """
        Update traffic light state based on YOLO detections.
        Args:
            detections (list): list of dicts like:
                { "class_id": int, "class_name": str, "confidence": float, "bbox": [x1, y1, x2, y2] }
        Returns:
            str: "red", "green", "yellow", or "unknown"
        """
        new_state = self.state  # keep previous by default

        for det in detections:
            cls = det["class_id"]

            # Adjust these IDs to match your YOLO model's classes
            if cls == 1:   # Red traffic light
                new_state = "red"
            elif cls == 2:  # Green traffic light
                new_state = "green"
            elif cls == 3:  # (Optional) Yellow light if your model detects it
                new_state = "yellow"

        # update only if a new state was found
        if new_state != self.state:
            print(f"Traffic light state changed: {self.state} -> {new_state}")
            self.state = new_state

        return self.state
