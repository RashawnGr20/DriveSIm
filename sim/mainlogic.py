import cv2 
import mediapipe as mp 
from headtracking import HeadTracker


cap = cv2.VideoCapture(0)
if not cap.isOpened() :
    print("cannot access camera")
    exit()

tracker = HeadTracker()
prev_smoothed = None 
while True: 
    ret, frame = cap.read() 
    if not ret:
        print("Can't receive frame (stream end?) Exiting...")
        break

    results = tracker.process_frame(frame)

    if results.multi_face_landmarks: 
        for face_landmarks in results.multi_face_landmarks:
            tracker.mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp.solutions.face_mesh.FACEMESH_TESSELATION
            )
    if results.multi_face_landmarks is None: 
        print("tracking lost")
        break; 
        if results.multi_face_landmarks: 
            for face_landmarks in results.multi_face_landmarks:
                raw_pos  = tracker.get_body_pos(face_landmarks)

                smoothed_pos = tracker.smoothed_points(raw_pos, prev_smoothed, 0.2)

                prev_smoothed = smoothed_pos

                vectors = tracker.pitch_vectors(smoothed_pos)

                pitch_angle = vectors["pitch_angle"]
                yaw_angle = vectors["yaw_angle"]
                roll_angle = vectors["roll_angle"]

                print(f"Pitch: {pitch_angle}, Yaw: {yaw_angle}, Roll: {roll_angle}")
    
    

    cv2.imshow("Camera Feed", frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()


