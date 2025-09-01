import numpy as np
import time

# Example: basic speed estimation based on displacement
class SpeedEstimator:
    def __init__(self, pixels_per_meter=10):
        self.last_positions = {}
        self.last_times = {}
        self.pixels_per_meter = pixels_per_meter

    def estimate(self, track_id, bbox):
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        now = time.time()

        if track_id in self.last_positions:
            dx = center_x - self.last_positions[track_id][0]
            dy = center_y - self.last_positions[track_id][1]
            dt = now - self.last_times[track_id]

            speed_mps = (np.sqrt(dx**2 + dy**2) / self.pixels_per_meter) / dt
            speed_kph = speed_mps * 3.6
        else:
            speed_kph = 0

        self.last_positions[track_id] = (center_x, center_y)
        self.last_times[track_id] = now
        return speed_kph
