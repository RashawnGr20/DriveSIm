# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

DriveSim ("LookFirst") is a desktop driver's-test prep tool: a webcam-driven head/eye-tracking
simulator (pygame + MediaPipe) that scores whether a user performs the correct mirror/blind-spot
checks during scripted driving scenarios, plus a FastAPI/Postgres backend for accounts and
session/gaze history.

The repo is really **two independent Python apps** sharing no code, each with its own venv and
dependency file:

- `sim/` — the pygame desktop client (computer vision + rendering + scenario logic). Deps in
  `requirements.txt` (repo root), venv in `drivesim_env/`.
- `backend/` — a FastAPI + SQLAlchemy/Postgres API for auth and session/gaze data. Deps in
  `backend/requirements.txt`, venv in `backend_env/`.

## Commands

Backend (run from repo root so the `backend.*` absolute imports resolve):
```
backend_env\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```
Requires `backend/.env` with `DATABASE_URL` (Postgres) and `SECRET_KEY` (JWT signing secret,
see `backend/auth/config.py`). `.env` is gitignored — never commit it.

Sim client:
```
drivesim_env\Scripts\activate
pip install -r requirements.txt
python sim/mainlogic.py
```
Needs a working webcam. The auth/login screens require the backend running locally at
`http://127.0.0.1:8000` (hardcoded in `sim/auth_client.py`); otherwise the sim can be used in
guest mode.

There is no test runner, linter, or build step configured for either half. `backend/auth/test.py`
and `sim/test_auth.py` are ad hoc manual scripts (not pytest), used for hashing a password and
hitting the live backend respectively — not part of any CI.

## Sim architecture (`sim/`)

`mainlogic.py` is the entry point: a single `while running` loop that both drives the
`SceneGen` state machine and — only while `scene.state` is `"calibration"` or `"simulation"` —
pulls camera frames, runs face tracking, classifies gaze/pose, evaluates scenario progress, and
renders. When state is anything else (home, scene_select, etc.) the loop just calls
`scene.update()` with no tracking args and releases the camera.

Pipeline for a tracked frame:
1. `HeadTracker` (`headtracking.py`) runs MediaPipe face mesh, smooths landmark positions, and
   derives pitch/yaw/roll (`pitch_vectors`) plus normalized iris/gaze offsets
   (`normalized_gaze`, `gaze_vectors`) used to render an eye-position cursor.
2. `feedBackEngine.assign_pose()` (`feedback.py`) maps pitch/yaw onto a fixed set of pose labels
   (`FORWARD`, `LEFT MIRROR`, `LEFT BLINDSPOT`, `RIGHT MIRROR`, `RIGHT BLINDSPOT`, `TOP MIRROR`,
   `LOOKING DOWN`) via hardcoded degree thresholds, debounced by a `pose_counter` (a pose must
   hold for 5 frames to become the `confirmed_pose`). This confirmed pose is the sole signal fed
   into scenario evaluation.
3. `Scene` / `SequenceScene` / `coverageScene` (`scenes.py`) evaluate the confirmed pose against
   a scenario's `expected_sequence`: `SequenceScene` requires an ordered checklist (each step
   needs `min_glance` consecutive frames), `coverageScene` requires touching a set of zones in
   any order. `Metrics.sequence_score` turns the per-step results into a 0–100 score shown on
   the results screen.
4. `SceneGen` (`scenegen.py`) + `UI` (`UI.py`) own the pygame window, screen state machine
   (`home`, `scene_select`, `about`, `features`, `auth`, `calibration`, `simulation`, `results`),
   click routing, and all drawing. `SceneGen.update()` dispatches to a `update_<state>` method
   per state.

Calibration (still inside the `mainlogic.py` main loop, driven by `scene.state == "calibration"`)
is two sequential sub-phases, tracked with module-level state, not an object:
- **Head baseline**: buffer ~60 frames of pitch/yaw/roll while the user holds still facing
  forward (rejecting the buffer and restarting if yaw spread is too high) to compute
  `baseline_angles`. All subsequent pitch/yaw/roll are reported relative to this baseline via
  `angle_diff_deg`.
- **Gaze calibration**: after a 30-frame warmup, walks `gaze_phase` through
  `center → left → right → up → down`, collecting eye samples via
  `HeadTracker.collect_gaze_sample` for each, then `HeadTracker.finalize_calibration()` builds
  the gaze-to-screen mapping used by `gaze_vectors` during simulation. On failure it resets back
  to the `center` phase.

Scenario metadata is defined in **two places that must be kept in sync**: `scenes.py` defines the
evaluation logic and `expected_sequence` per scenario key, while `SceneGen.scene_info` in
`scenegen.py` separately holds the display title/description/required-checks/images for the same
scenario keys (used by the scene-select and scene-intro screens).

## Backend architecture (`backend/`)

Standard FastAPI layout: `main.py` creates the app, calls `Base.metadata.create_all(engine)`, and
mounts routers. Data model (`backend/database/models.py`): `User` 1:N `Session` 1:N `GazeEvent`,
plain SQLAlchemy declarative models against Postgres via `DATABASE_URL`.

Auth (`backend/auth/`) is JWT-based: `security.py` hashes/verifies passwords with passlib/bcrypt,
`tokens.py` issues a JWT (`python-jose`) carrying `user_id` with an expiry, `dependencies.py`
decodes the bearer token via `OAuth2PasswordBearer` to resolve the current `User`.

`backend/gaze/router.py` is **not mounted** in `main.py` (only `auth_router` and `session_router`
are included) and its import of `get_current_user` is `from auth.dependencies import ...` rather
than `backend.auth.dependencies`, so it will fail if wired up as-is — treat gaze-event logging as
unfinished/dead code rather than a working endpoint.

`sim/auth_client.py` is the only consumer of the backend from the sim side (login/signup against
`http://127.0.0.1:8000/auth/...`); session/gaze logging from the sim client isn't wired up yet.
