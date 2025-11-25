import cv2 
import mediapipe as mp 
from headtracking import HeadTracker


cap = cv2.VideoCapture(0)
if not cap.isOpened() :
    print("cannot access camera")
    exit()

tracker = HeadTracker()

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

    if results.multi_face_landmarks: 
        for face_landmarks in results.multi_face_landmarks:
            pos  = tracker.get_body_pos(face_landmarks)

            tracker.print_landmarks(pos)

    cv2.imshow("Camera Feed", frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()


