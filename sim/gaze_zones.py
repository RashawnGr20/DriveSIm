from dataclasses import dataclass
import math

MIN_BASELINE_RADIUS = 0.15
BASELINE_STDDEV_MULTIPLIER = 3.0
BASELINE_ANCHOR_CAP_RATIO = 0.9


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


def _distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class GazeZoneClassifier:

    def __init__(self):
        self._anchors = {}
        self._forward_baseline = None

    def register_anchor(self, name, gaze_samples):
        if not gaze_samples:
            return None

        (mean_x, mean_y), _ = _mean_and_stddev(gaze_samples)
        anchor = ZoneAnchor(name=name, gaze_xy=(mean_x, mean_y))
        self._anchors[name] = anchor
        print("[zones] anchor", name, "gaze=", anchor.gaze_xy)
        return anchor

    def set_forward_baseline(self, gaze_samples):
        if not gaze_samples:
            return None

        (mean_x, mean_y), stddev = _mean_and_stddev(gaze_samples)
        raw_radius = max(BASELINE_STDDEV_MULTIPLIER * stddev, MIN_BASELINE_RADIUS)

        self._forward_baseline = ForwardBaseline(gaze_xy=(mean_x, mean_y), radius=raw_radius)
        print("[zones] forward baseline gaze=", (mean_x, mean_y), "raw_radius=", raw_radius)
        return self._forward_baseline

    def finalize_anchors(self):
        if self._forward_baseline is not None and self._anchors:
            baseline_pos = self._forward_baseline.gaze_xy
            nearest_distance = min(
                _distance(baseline_pos, a.gaze_xy) for a in self._anchors.values()
            )
            capped = min(self._forward_baseline.radius, BASELINE_ANCHOR_CAP_RATIO * nearest_distance)
            if capped != self._forward_baseline.radius:
                print("[zones] cap forward_baseline from",
                      self._forward_baseline.radius, "to", capped)
                self._forward_baseline.radius = capped

        print("[zones] --- calibration dump ---")
        if self._forward_baseline is not None:
            print("[zones] baseline mean=", self._forward_baseline.gaze_xy,
                  "radius=", self._forward_baseline.radius)
        for name, anchor in self._anchors.items():
            print("[zones] anchor", name, "pos=", anchor.gaze_xy)
        names = list(self._anchors.keys())
        for i, a_name in enumerate(names):
            a_pos = self._anchors[a_name].gaze_xy
            if self._forward_baseline is not None:
                print("[zones] dist", a_name, "-> baseline =",
                      _distance(a_pos, self._forward_baseline.gaze_xy))
            for b_name in names[i + 1:]:
                b_pos = self._anchors[b_name].gaze_xy
                print("[zones] dist", a_name, "->", b_name, "=", _distance(a_pos, b_pos))
        print("[zones] --- end dump ---")

    def classify(self, norm_x, norm_y):
        if norm_x is None or norm_y is None or not self._anchors:
            return None

        if self.is_at_forward_baseline(norm_x, norm_y):
            return None

        best_name = None
        best_distance = float("inf")

        for name, anchor in self._anchors.items():
            distance = _distance((norm_x, norm_y), anchor.gaze_xy)
            if distance < best_distance:
                best_name = name
                best_distance = distance

        return best_name

    def is_at_forward_baseline(self, norm_x, norm_y):
        if norm_x is None or norm_y is None or self._forward_baseline is None:
            return False
        return _distance((norm_x, norm_y), self._forward_baseline.gaze_xy) < self._forward_baseline.radius

    def has_anchor(self, name):
        return name in self._anchors

    def clear(self):
        self._anchors.clear()
        self._forward_baseline = None
