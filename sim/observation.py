DEFAULT_STABILITY_FRAMES = 5


class ObservationEngine:

    def __init__(self, classifier, stability_frames=DEFAULT_STABILITY_FRAMES):
        self.classifier = classifier
        self.stability_frames = stability_frames

        self.last_zone = "FORWARD"
        self.zone_counter = 0
        self.confirmed_zone = "FORWARD"

    def reset(self):
        self.last_zone = "FORWARD"
        self.zone_counter = 0
        self.confirmed_zone = "FORWARD"

    def estimate_zone(self, head_pose, gaze_x=None, gaze_y=None):
        gaze_zone = self.classifier.classify(gaze_x, gaze_y)

        if head_pose == "FORWARD":
            return gaze_zone if gaze_zone is not None else "FORWARD"

        if not self.classifier.has_anchor(head_pose):
            return head_pose

        if gaze_zone == head_pose:
            return head_pose

        if self.classifier.is_at_forward_baseline(gaze_x, gaze_y):
            return "FORWARD"

        return head_pose

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
