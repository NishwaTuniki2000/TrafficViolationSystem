import numpy as np
import time
from collections import deque

class SpeedEstimator:
    def __init__(self, pixels_per_meter=10, window_size=5):
        self.last_positions = {}
        self.last_times = {}
        self.speed_history = {}
        self.pixels_per_meter = pixels_per_meter
        self.window_size = window_size

    def estimate(self, track_id, bbox):
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        now = time.time()

        speed_kph = 0
        if track_id in self.last_positions:
            dx = center_x - self.last_positions[track_id][0]
            dy = center_y - self.last_positions[track_id][1]
            dt = now - self.last_times[track_id]

            if dt > 0:
                speed_mps = (np.sqrt(dx**2 + dy**2) / self.pixels_per_meter) / dt
                speed_kph = speed_mps * 3.6

        # maintain speed history for smoothing
        if track_id not in self.speed_history:
            self.speed_history[track_id] = deque(maxlen=self.window_size)
        self.speed_history[track_id].append(speed_kph)

        # save latest position/time
        self.last_positions[track_id] = (center_x, center_y)
        self.last_times[track_id] = now

        return float(np.mean(self.speed_history[track_id]))
