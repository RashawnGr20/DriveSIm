from dataclasses import dataclass
import math

MIN_RADIUS = 0.10
STDDEV_MULTIPLIER = 3.0


@dataclass(frozen=True)
class ZoneSpec:
    name: str
    screen_pos: tuple
    calibration_prompt: str


ZONE_CATALOG = [
    ZoneSpec(
        name="TOP MIRROR",
        screen_pos=(0.5, 0.08),
        calibration_prompt="Look at the top mirror",
    ),
]


@dataclass
class ZoneAnchor:
    name: str
    gaze_xy: tuple
    radius: float


class GazeZoneClassifier:

    def __init__(self):
        self._anchors = {}

    def register_anchor(self, name, gaze_samples):
        if not gaze_samples:
            return None

        mean_x = sum(x for x, y in gaze_samples) / len(gaze_samples)
        mean_y = sum(y for x, y in gaze_samples) / len(gaze_samples)

        if len(gaze_samples) >= 2:
            var_x = sum((x - mean_x) ** 2 for x, y in gaze_samples) / len(gaze_samples)
            var_y = sum((y - mean_y) ** 2 for x, y in gaze_samples) / len(gaze_samples)
            stddev = math.sqrt(var_x + var_y)
        else:
            stddev = 0.0

        radius = max(STDDEV_MULTIPLIER * stddev, MIN_RADIUS)

        anchor = ZoneAnchor(name=name, gaze_xy=(mean_x, mean_y), radius=radius)
        self._anchors[name] = anchor
        print("[zones] anchor", name, "gaze=", anchor.gaze_xy, "radius=", radius)
        return anchor

    def classify(self, norm_x, norm_y):
        if norm_x is None or norm_y is None or not self._anchors:
            return None

        best_name = None
        best_distance = float("inf")

        for name, anchor in self._anchors.items():
            ax, ay = anchor.gaze_xy
            distance = math.sqrt((norm_x - ax) ** 2 + (norm_y - ay) ** 2)
            if distance < anchor.radius and distance < best_distance:
                best_name = name
                best_distance = distance

        return best_name

    def has_anchor(self, name):
        return name in self._anchors

    def clear(self):
        self._anchors.clear()
