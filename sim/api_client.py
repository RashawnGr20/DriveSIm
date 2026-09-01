import requests
from auth_client import BASE_URL


class ApiClient:

    def __init__(self, auth_client):
        self.auth_client = auth_client

    def _headers(self):
        return {"Authorization": f"Bearer {self.auth_client.token}"}

    def create_session(self, scenario, scenario_type, expected_sequence):
        try:
            resp = requests.post(f"{BASE_URL}/sessions/", json={
                "scenario": scenario,
                "scenario_type": scenario_type,
                "expected_sequence": expected_sequence,
            }, headers=self._headers())
            if resp.status_code == 200:
                return resp.json().get("session_id")
        except requests.exceptions.RequestException as e:
            print("create_session failed:", e)
        return None

    def post_gaze_batch(self, session_id, events):
        if session_id is None:
            return
        try:
            requests.post(f"{BASE_URL}/gaze/batch", json={
                "session_id": session_id,
                "events": events,
            }, headers=self._headers())
        except requests.exceptions.RequestException as e:
            print("post_gaze_batch failed:", e)

    def complete_session(self, session_id, score, step_results):
        if session_id is None:
            return
        try:
            requests.post(f"{BASE_URL}/sessions/{session_id}/complete", json={
                "score": score,
                "step_results": step_results,
            }, headers=self._headers())
        except requests.exceptions.RequestException as e:
            print("complete_session failed:", e)
