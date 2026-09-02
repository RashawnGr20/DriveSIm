DEFAULT_UP_THRESHOLD = 0.15
DEFAULT_STABILITY_FRAMES = 5


class ObservationEngine:

    def __init__(self, up_threshold=DEFAULT_UP_THRESHOLD, stability_frames=DEFAULT_STABILITY_FRAMES):
        self.up_threshold = up_threshold
        self.stability_frames = stability_frames

        self.gaze_forward_y = None

        self.last_zone = "FORWARD"
        self.zone_counter = 0
        self.confirmed_zone = "FORWARD"

    def set_gaze_forward_baseline(self, norm_y):
        self.gaze_forward_y = norm_y
        print("[obs] forward baseline:", norm_y)

    def reset(self):
        self.last_zone = "FORWARD"
        self.zone_counter = 0
        self.confirmed_zone = "FORWARD"

    def _is_gaze_upward(self, gaze_y):
        if gaze_y is None or self.gaze_forward_y is None:
            return False
        return (gaze_y - self.gaze_forward_y) < -self.up_threshold

    def estimate_zone(self, head_pose, gaze_x=None, gaze_y=None):
        if head_pose != "FORWARD":
            return head_pose

        if self._is_gaze_upward(gaze_y):
            return "TOP MIRROR"

        return "FORWARD"

    def update(self, head_pose, gaze_x=None, gaze_y=None):
        zone = self.estimate_zone(head_pose, gaze_x, gaze_y)

        if zone == self.last_zone:
            self.zone_counter += 1
        else:
            self.zone_counter = 1
        self.last_zone = zone

        if self.zone_counter >= self.stability_frames:
            prev_confirmed = self.confirmed_zone
            self.confirmed_zone = zone
            if zone != prev_confirmed:
                print("[obs] confirmed zone:", prev_confirmed, "->", zone)

        return self.confirmed_zone
