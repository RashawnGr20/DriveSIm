import pygame
import cv2
import mediapipe as mp

from headtracking import HeadTracker
from feedback import feedBackEngine
from scenegen import SceneGen
from scenes import Scene, Metrics
from UI import UI


scene = SceneGen(1920, 1080, 60)
ui = UI(scene.screen, scene.W, scene.H)
scene.ui = ui
scene.selected_scene = "left_lane_change"
scene.state = "home"

scene_manager = None
metrics = None
cap = None
tracker = None
feedback = None


prev_smoothed = None
prev_angles = None
prev_prev_angles = None
baseline_angles = None
baseline_buffer = []
BASELINE_FRAMES = 60
prev_rel = None
prev_prev_rel = None
prev_gaze = (0.0, 0.0)
gaze_calibrated = False 
gaze_warmup_frames = 30
gaze_warmup_count = 0

DEADZONE_PITCH = 2
DEADZONE_YAW = 1
DEADZONE_ROLL = 1


def apply_deadzone(angle, threshold):
    distance = max(0, abs(angle) - threshold)
    sign = 1 if angle >= 0 else -1
    return sign * distance


def clamp(x, upper):
    return max(-upper, min(upper, x))


def angle_diff_deg(a, b):
    return (a - b + 180) % 360 - 180


running = True
simulation_initialized = False

while running:

    if scene.state not in {"simulation", "calibration"}:
        if simulation_initialized:
            if cap is not None:
                cap.release()
                cap = None
            cv2.destroyAllWindows()
            simulation_initialized = False

        running = scene.update()
        continue

    if scene.state in {"simulation", "calibration"} and not simulation_initialized:
        scene_manager = Scene(scene.selected_scene)
        metrics = Metrics(scene_manager.current_scene.expected_sequence)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("cannot access camera")
            break

        tracker = HeadTracker()
        feedback = feedBackEngine()
        tracker.reset_gaze()

        prev_smoothed = None
        prev_angles = None
        prev_prev_angles = None
        baseline_angles = None
        baseline_buffer = []
        prev_rel = None
        prev_prev_rel = None
        prev_gaze = (0.0, 0.0)
        simulation_initialized = True
        gaze_calibrated = False 
        gaze_warmup_frames = 30
        gaze_warmup_count = 0           
        

    ret, frame = cap.read()
    if not ret:
        break

    results = tracker.process_frame(frame)

    if not results.multi_face_landmarks:
        if prev_angles and prev_prev_angles:
            final_pitch = prev_angles["pitch"] + (prev_angles["pitch"] - prev_prev_angles["pitch"])
            final_yaw = prev_angles["yaw"] + (prev_angles["yaw"] - prev_prev_angles["yaw"])
            final_roll = prev_angles["roll"] + (prev_angles["roll"] - prev_prev_angles["roll"])
        elif prev_angles:
            final_pitch = prev_angles["pitch"]
            final_yaw = prev_angles["yaw"]
            final_roll = prev_angles["roll"]
        else:
            final_pitch, final_yaw, final_roll = 0, 0, 0

        final_pitch = apply_deadzone(final_pitch, DEADZONE_PITCH)
        final_yaw = apply_deadzone(final_yaw, DEADZONE_YAW)
        final_roll = apply_deadzone(final_roll, DEADZONE_ROLL)

        pose = feedback.update(final_pitch, final_yaw, final_roll)
        progress_data = scene_manager.get_progress_data()
        offset_x, offset_y = prev_gaze

        running = scene.update(final_pitch, final_yaw, final_roll, pose, offset_x, offset_y, progress_data)
        if not running:
            break

        cv2.imshow("Camera Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        continue

    for face_landmarks in results.multi_face_landmarks:
        tracker.mp_drawing.draw_landmarks(
            frame,
            face_landmarks,
            mp.solutions.face_mesh.FACEMESH_TESSELATION
        )

        raw_pos = tracker.get_body_pos(face_landmarks)
        smoothed_pos = tracker.smoothed_points(raw_pos, prev_smoothed, 0.2)

        vectors = tracker.pitch_vectors(smoothed_pos)
        pitch = vectors["pitch_angle"]
        yaw = vectors["yaw_angle"]
        roll = vectors["roll_angle"]

        if scene.state == "calibration" : 
            if baseline_angles is None:
                baseline_buffer.append((pitch, yaw, roll))

                if len(baseline_buffer) >= 5:
                    recent = baseline_buffer[-5:]
                    spread_yaw = max(y for _, y, _ in recent) - min(y for _, y, _ in recent)
                    if spread_yaw > 4:
                        baseline_buffer.clear()
                        prev_smoothed = smoothed_pos
                        continue
                
                
                head_progress = min(1.0, len(baseline_buffer) / BASELINE_FRAMES)
                calibration_progress_data = {
                    "progress": 0.6 * head_progress, 
                    "status_text": "Hold still and face forward"
                }

                running = scene.update(0,0,0, "FORWARD", 0.0, 0.0, progress_data)
                if not running : 
                    break 


                if len(baseline_buffer) < BASELINE_FRAMES:
                    
                    prev_smoothed = smoothed_pos
                    continue

                avg_pitch = sum(p for p, _, _ in baseline_buffer) / BASELINE_FRAMES
                avg_yaw = sum(y for _, y, _ in baseline_buffer) / BASELINE_FRAMES
                avg_roll = sum(r for _, _, r in baseline_buffer) / BASELINE_FRAMES

                baseline_angles = {
                    "pitch": avg_pitch,
                    "yaw": avg_yaw,
                    "roll": avg_roll
                }

                tracker.reset_gaze()
                gaze_calibrated = False 
                prev_gaze = (0.0, 0.0)
                gaze_warmup_count = 0

                prev_angles = {"pitch": 0, "yaw": 0, "roll": 0}
                prev_prev_angles = None
                prev_rel = {"pitch": 0, "yaw": 0, "roll": 0}
                prev_prev_rel = None
                prev_smoothed = smoothed_pos

                continue

            if not gaze_calibrated : 

                if gaze_warmup_count < gaze_warmup_frames : 
                    gaze_warmup_count += 1
                    
                    
                    gaze_progress = min(1.0, gaze_warmup_count / gaze_warmup_frames)
                    progress_data = {
                        "progress": 0.6 + 0.4 * gaze_progress, 
                        "status_text": "Look directly at the center dot"
                    } 
                    
                    running = scene.update(0,0,0, pose, 0.0, 0.0, progress_data)

                    if not running :
                        break

                    prev_smoothed = smoothed_pos
                    continue 
                    
                    

                norm_x, norm_y = tracker.normalized_gaze(face_landmarks)
                gaze_calibrated = tracker.update_gaze_baseline(norm_x, norm_y)
                
                calibration_progress_data = {
                    "progress": 1.0 if gaze_calibrated else 0.95,
                    "status_text": "Calibration complete" if gaze_calibrated else "Look directly at the center point"
                }
                
                running = scene.update(0,0,0, pose, 0.0, 0.0, progress_data)

                if not running : 
                    break 
                
                prev_gaze = (0.0, 0.0)
                prev_smoothed = smoothed_pos

                if gaze_calibrated : 
                    scene.state = "simulation"
                    scene.start_fade_in()

                continue 

    
        print("CURRENT BASELINE:", tracker.gaze_baseline)
        norm_x, norm_y = tracker.normalized_gaze(face_landmarks)
        offset_x, offset_y = tracker.gaze_vectors(norm_x, norm_y)
        prev_gaze = (offset_x, offset_y)

        rel_pitch = angle_diff_deg(pitch, baseline_angles["pitch"])
        rel_yaw = angle_diff_deg(yaw, baseline_angles["yaw"])
        rel_roll = angle_diff_deg(roll, baseline_angles["roll"])

        final_pitch, final_yaw, final_roll = rel_pitch, rel_yaw, rel_roll

        final_pitch = apply_deadzone(final_pitch, DEADZONE_PITCH)
        final_yaw = apply_deadzone(final_yaw, DEADZONE_YAW)
        final_roll = apply_deadzone(final_roll, DEADZONE_ROLL)

        pose = feedback.update(final_pitch, final_yaw, final_roll)
        progress_data = scene_manager.get_progress_data()

        print("final render offsets:", offset_x, offset_y)
        print("gaze_calibrated:", gaze_calibrated)

        running = scene.update(final_pitch, final_yaw, final_roll, pose, offset_x, offset_y, progress_data)
        if not running:
            break

        prev_prev_rel = prev_rel.copy() if prev_rel else None
        prev_rel = {"pitch": rel_pitch, "yaw": rel_yaw, "roll": rel_roll}

        prev_prev_angles = prev_angles.copy() if prev_angles else None
        prev_angles = {"pitch": final_pitch, "yaw": final_yaw, "roll": final_roll}

        prev_smoothed = smoothed_pos

        pose_counter = feedback.pose_counter
        outcome =  scene_manager.evaluation(pose_counter, pose)

        if outcome and outcome["finished"] : 
            result = outcome["result"]
            score = metrics.sequence_score(result)

            scene.last_score = score
            scene.last_result = result 
            scene.state = "results"
            scene.start_fade_in()

            continue 

    cv2.imshow("Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

if cap is not None:
    cap.release()

cv2.destroyAllWindows()
pygame.quit()