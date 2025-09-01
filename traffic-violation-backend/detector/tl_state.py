# Simple FSM to track red/green traffic light state over time
class TrafficLightState:
    def __init__(self):
        self.state = "unknown"

    def update(self, detections):
        for det in detections:
            cls = det["class_id"]
            if cls == 1:  # assuming 1 = red light
                self.state = "red"
            elif cls == 2:  # assuming 2 = green light
                self.state = "green"
        return self.state
