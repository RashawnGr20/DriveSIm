import cv2
import mediapipe as mp
from headtracking import HeadTracker
from feedback import feedBackEngine
from scenegen import SceneGen


import os
print(os.getcwd())

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("cannot access camera")
    exit()

tracker = HeadTracker()
feedback = feedBackEngine()
scene = SceneGen(1280,720,60)

prev_smoothed = None
prev_angles = None
prev_prev_angles = None
baseline_angles = None 
baseline_buffer = []
BASELINE_FRAMES = 60 
prev_rel = None
prev_prev_rel = None

DEADZONE_PITCH = 3
DEADZONE_YAW = 3
DEADZONE_ROLL = 3

def apply_deadzone(angle, threshold): 
    if abs(angle) < threshold :
        return 0 
    return angle 

def clamp(x, upper) :
    return max(-upper, min(upper, x))

def angle_diff_deg(a, b) : 

    return (a-b + 180) % 360 - 180


while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = tracker.process_frame(frame)

    if not results.multi_face_landmarks:
        if prev_angles and prev_prev_angles:
            final_pitch = prev_angles["pitch"] + (prev_angles["pitch"] - prev_prev_angles["pitch"])
            final_yaw   = prev_angles["yaw"]   + (prev_angles["yaw"]   - prev_prev_angles["yaw"])
            final_roll  = prev_angles["roll"]  + (prev_angles["roll"]  - prev_prev_angles["roll"])

        elif prev_angles :
            final_pitch, final_yaw, final_roll = prev_angles["pitch"], prev_angles["yaw"], prev_angles["roll"]   
            
        else :
            final_pitch, final_yaw, final_roll = 0,0,0
            
           
        final_pitch = apply_deadzone(final_pitch,DEADZONE_PITCH)
        final_yaw = apply_deadzone(final_yaw,DEADZONE_YAW)
        final_roll = apply_deadzone(final_roll,DEADZONE_ROLL)

        pose = feedback.update(final_pitch, final_yaw, final_roll)
            
        if not scene.update(final_pitch, final_yaw, final_roll, pose):
            break; 
                
        print(f"Pitch: {final_pitch:.2f}, Yaw: {final_yaw:.2f}, Roll: {final_roll:.2f}, Pose: {pose}")

        cv2.imshow("Camera Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
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
        yaw   = vectors["yaw_angle"]
        roll  = vectors["roll_angle"]

        print(f"RAW:     pitch={pitch:.2f}, yaw={yaw:.2f}, roll={roll:.2f},")


        if baseline_angles is None : 
            baseline_buffer.append((pitch, yaw, roll))

            if len(baseline_buffer) >= 5 : 
                recent = baseline_buffer[-5:]
                spread_yaw = max(y for _, y, _ in recent) - min(y for _, y, _ in recent)
                if spread_yaw > 4 :
                    baseline_buffer.clear()
                    prev_smoothed = smoothed_pos
                    continue

            if len(baseline_buffer) < BASELINE_FRAMES:
                prev_smoothed = smoothed_pos
                continue

            avg_pitch = sum(p for p, _, _ in baseline_buffer) / BASELINE_FRAMES
            avg_yaw   = sum(y for _, y, _ in baseline_buffer) / BASELINE_FRAMES
            avg_roll  = sum(r for _, _, r in baseline_buffer) / BASELINE_FRAMES

            baseline_angles = {
                "pitch": avg_pitch, 
                 "yaw": avg_yaw,
                "roll": avg_roll         
            }

            print(f"BASELINE set: pitch={avg_pitch:.2f}, yaw={avg_yaw:.2f}, roll={avg_roll:.2f},")
            prev_angles = {"pitch": 0, "yaw": 0, "roll": 0}
            prev_prev_angles = None

            prev_rel = {"pitch": 0, "yaw": 0, "roll": 0}
            prev_prev_rel = None


            prev_smoothed = smoothed_pos
            continue

        rel_pitch = angle_diff_deg(pitch, baseline_angles["pitch"])
        rel_yaw =  angle_diff_deg(yaw, baseline_angles["yaw"])
        rel_roll = angle_diff_deg(roll, baseline_angles["roll"])

        print(f"REL    set: pitch={rel_pitch:.2f}, yaw={rel_yaw:.2f}, roll={rel_roll:.2f},")
    
        if prev_rel and prev_prev_rel:
            dp = clamp(prev_rel["pitch"] - prev_prev_rel["pitch"], 3)
            dy = clamp(prev_rel["yaw"] - prev_prev_rel["yaw"], 3)
            dr = clamp(prev_rel["roll"] - prev_prev_rel["roll"], 3)


            final_pitch = rel_pitch + dp
            final_yaw = rel_yaw + dy
            final_roll = rel_roll+ dr

        else:
            final_pitch, final_yaw, final_roll = rel_pitch, rel_yaw, rel_roll
        
        final_pitch = apply_deadzone(final_pitch,DEADZONE_PITCH)
        final_yaw = apply_deadzone(final_yaw,DEADZONE_YAW)
        final_roll = apply_deadzone(final_roll,DEADZONE_ROLL)

        pose = feedback.update(final_pitch, final_yaw, final_roll)
        
        if not scene.update(final_pitch, final_yaw, final_roll, pose):
            cap.release()
            cv2.destroyAllWindows()
            break

        prev_prev_rel = prev_rel.copy() if prev_rel else None 
        prev_rel = {"pitch": rel_pitch, "yaw": rel_yaw, "roll": rel_roll}

        prev_prev_angles = prev_angles.copy() if prev_angles else None
        prev_angles = {"pitch": final_pitch, "yaw": final_yaw, "roll": final_roll}
        
        prev_smoothed = smoothed_pos

        print(f"FINAL     Pitch: {final_pitch:.2f}, Yaw: {final_yaw:.2f}, Roll: {final_roll:.2f}, Pose: {pose}")

    cv2.imshow("Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()       
