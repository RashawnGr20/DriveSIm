class SessionRecorder:

    BATCH_SIZE = 20

    def __init__(self, api_client, session_id):
        self.api_client = api_client
        self.session_id = session_id
        self.buffer = []
        self._segment_pose = None
        self._segment_start = None

    def on_pose(self, confirmed_pose, yaw, pitch, now):
        if self._segment_pose is None:
            self._segment_pose, self._segment_start = confirmed_pose, now
            return

        if confirmed_pose != self._segment_pose:
            self._emit(self._segment_pose, yaw, pitch, now - self._segment_start)
            self._segment_pose, self._segment_start = confirmed_pose, now

    def _emit(self, pose, yaw, pitch, duration):
        self.buffer.append({
            "pose": pose,
            "yaw": yaw,
            "pitch": pitch,
            "duration": duration,
        })
        if len(self.buffer) >= self.BATCH_SIZE:
            self.flush()

    def flush(self):
        if self.buffer:
            self.api_client.post_gaze_batch(self.session_id, self.buffer)
            self.buffer.clear()

    def finalize(self, yaw, pitch, now):
        if self._segment_pose is not None:
            self._emit(self._segment_pose, yaw, pitch, now - self._segment_start)
        self.flush()
