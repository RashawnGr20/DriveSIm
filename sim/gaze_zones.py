from dataclasses import dataclass
import math

MIN_RADIUS = 0.10
STDDEV_MULTIPLIER = 3.0
NEIGHBOR_CAP_RATIO = 0.45


@dataclass(frozen=True)
class ZoneSpec:
    name: str
    screen_pos: tuple
    calibration_prompt: str


ZONE_CATALOG = [
    ZoneSpec("TOP MIRROR",   (0.5,  0.08), "Look at the top mirror"),
    ZoneSpec("LEFT MIRROR",  (0.05, 0.55), "Look at the left side mirror"),
    ZoneSpec("RIGHT MIRROR", (0.95, 0.55), "Look at the right side mirror"),
    ZoneSpec("LOOKING DOWN", (0.5,  0.92), "Look at the dashboard"),
]


@dataclass
class ZoneAnchor:
    name: str
    gaze_xy: tuple
    radius: float


@dataclass
class ForwardBaseline:
    gaze_xy: tuple
    radius: float


def _mean_and_stddev(samples):
    n = len(samples)
    if n == 0:
        return (0.0, 0.0), 0.0
    mean_x = sum(x for x, y in samples) / n
    mean_y = sum(y for x, y in samples) / n
    if n < 2:
        return (mean_x, mean_y), 0.0
    var_x = sum((x - mean_x) ** 2 for x, y in samples) / n
    var_y = sum((y - mean_y) ** 2 for x, y in samples) / n
    return (mean_x, mean_y), math.sqrt(var_x + var_y)


class GazeZoneClassifier:

    def __init__(self):
        self._anchors = {}
        self._forward_baseline = None

    def register_anchor(self, name, gaze_samples):
        if not gaze_samples:
            return None

        (mean_x, mean_y), stddev = _mean_and_stddev(gaze_samples)
        radius = max(STDDEV_MULTIPLIER * stddev, MIN_RADIUS)

        anchor = ZoneAnchor(name=name, gaze_xy=(mean_x, mean_y), radius=radius)
        self._anchors[name] = anchor
        print("[zones] anchor", name, "gaze=", anchor.gaze_xy, "raw_radius=", radius)
        return anchor

    def set_forward_baseline(self, gaze_samples):
        if not gaze_samples:
            return None

        (mean_x, mean_y), stddev = _mean_and_stddev(gaze_samples)
        radius = max(STDDEV_MULTIPLIER * stddev, MIN_RADIUS)

        self._forward_baseline = ForwardBaseline(gaze_xy=(mean_x, mean_y), radius=radius)
        print("[zones] forward baseline gaze=", (mean_x, mean_y), "raw_radius=", radius)
        return self._forward_baseline

    def _capped_radius(self, position, raw_radius, others):
        cap = raw_radius
        for other in others:
            ox, oy = other
            d = math.sqrt((position[0] - ox) ** 2 + (position[1] - oy) ** 2)
            if d > 0:
                cap = min(cap, NEIGHBOR_CAP_RATIO * d)
        return cap

    def finalize_anchors(self):
        anchor_positions = {name: a.gaze_xy for name, a in self._anchors.items()}

        for name, anchor in self._anchors.items():
            neighbors = [pos for other_name, pos in anchor_positions.items() if other_name != name]
            if self._forward_baseline is not None:
                neighbors.append(self._forward_baseline.gaze_xy)
            capped = self._capped_radius(anchor.gaze_xy, anchor.radius, neighbors)
            if capped != anchor.radius:
                print("[zones] cap", name, "from", anchor.radius, "to", capped)
            anchor.radius = capped

        if self._forward_baseline is not None:
            neighbors = list(anchor_positions.values())
            capped = self._capped_radius(self._forward_baseline.gaze_xy, self._forward_baseline.radius, neighbors)
            if capped != self._forward_baseline.radius:
                print("[zones] cap forward_baseline from", self._forward_baseline.radius, "to", capped)
            self._forward_baseline.radius = capped

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

    def is_at_forward_baseline(self, norm_x, norm_y):
        if norm_x is None or norm_y is None or self._forward_baseline is None:
            return False
        fx, fy = self._forward_baseline.gaze_xy
        distance = math.sqrt((norm_x - fx) ** 2 + (norm_y - fy) ** 2)
        return distance < self._forward_baseline.radius

    def has_anchor(self, name):
        return name in self._anchors

    def clear(self):
        self._anchors.clear()
        self._forward_baseline = None
