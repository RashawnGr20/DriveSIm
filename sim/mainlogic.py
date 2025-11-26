import cv2 
import mediapipe as mp 
from headtracking import HeadTracker


cap = cv2.VideoCapture(0)
if not cap.isOpened() :
    print("cannot access camera")
    exit()

tracker = HeadTracker()
prev_smoothed = None
prev_angles = None 
prev_prev_angles = None

while True: 
    ret, frame = cap.read() 
    if not ret:
        print("Can't receive frame (stream end?) Exiting...")
        break

    results = tracker.process_frame(frame)

    if not results.multi_face_landmarks: 
        if prev_smoothed is not None :
            vectors =  vectors = tracker.pitch_vectors(prev_smoothed)
            print(f"Pitch: {vectors['pitch_angle']}, Yaw: {vectors['yaw_angle']}, Roll: {vectors['roll_angle']}")
        cv2.imshow("Camera feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue
    
  
    for face_landmarks in results.multi_face_landmarks:
            tracker.mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp.solutions.face_mesh.FACEMESH_TESSELATION
            )
   
    
    for face_landmarks in results.multi_face_landmarks:
        raw_pos  = tracker.get_body_pos(face_landmarks)
        smoothed_pos = tracker.smoothed_points(raw_pos, prev_smoothed, 0.2)

        vectors = tracker.pitch_vectors(smoothed_pos)
        pitch_angle = vectors['pitch_angle']
        yaw_angle = vectors['yaw_angle']
        roll_angle = vectors['roll_angle']

        if prev_angles is not None and prev_prev_angles is not None : 
            predicted_pitch = pitch_angle + (pitch_angle - prev_prev_angles["pitch"])
            predicted_yaw = yaw_angle + (yaw_angle - prev_prev_angles["yaw"])
            predicted_roll = roll_angle + (roll_angle - prev_prev_angles["roll"])
        else :
            predicted_pitch = pitch_angle
            predicted_yaw = yaw_angle
            predicted_roll = roll_angle
        
        prev_prev_angles = prev_angles.copy() if prev_angles else None 
        prev_angles = {"pitch": pitch_angle, "yaw": yaw_angle, "roll": roll_angle}
        prev_smoothed = smoothed_pos

        print(f"Pitch: {predicted_pitch:.2f}, Yaw: {predicted_yaw:.2f}, Roll: {predicted_roll:.2f}")
    
    else:
        if prev_angles is not None and prev_prev_angles is not None : 
            predicted_pitch = prev_angles["pitch"] + (prev_angles["pitch"] - prev_prev_angles["pitch"])
            predicted_yaw = prev_angles["yaw"] + (prev_angles["yaw"] - prev_prev_angles["yaw"])
            predicted_roll = prev_angles["roll"] + (prev_angles["roll"] - prev_prev_angles["roll"])
            print(f"Pitch: {predicted_pitch:.2f}, Yaw: {predicted_yaw:.2f}, Roll: {predicted_roll:.2f}")

    cv2.imshow("Camera Feed", frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()


