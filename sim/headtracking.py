import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh 

class HeadTracker:
    def __init__(self, max_faces=1, min_detection_confidence=0.5,  min_tracking_confidence = 0.5):
        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=max_faces,
            refine_landmarks=True, 
            min_detection_confidence = min_detection_confidence,
           min_tracking_confidence =  min_tracking_confidence 
        )
        self.mp_drawing =  mp.solutions.drawing_utils

        def process_frame(self, frame) :
                
            import cv2

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame) 
            return results 
        
        def get_body_pos (self, face_landmarks ) :
            print(self)