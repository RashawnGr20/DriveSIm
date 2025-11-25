import mediapipe as mp
import cv2
from collections import namedtuple

mp_face_mesh = mp.solutions.face_mesh 
point3D = namedtuple("Point3D", ["x", "y", "z"])

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
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame) 
            return results 
        

    
    def get_body_pos (self, face_landmarks ) :
        
        
        nose = face_landmarks.landmark[1]
        chin = face_landmarks.landmark[152]
        forehead = face_landmarks.landmark[10]
        cheek = face_landmarks.landmark[454]
    
        return { 
            "Nose": point3D(nose.x, nose.y, nose.z),
            "Forehead": point3D(forehead.x, forehead.y, forehead.z),
            "Chin": point3D(chin.x, chin.y, chin.z),
            "Cheek": point3D(cheek.x, cheek.y, cheek.z)
        }

    def draw_landmarks(self, frame, face_landmarks) :
             self.mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp.solutions.face_mesh.FACEMESH_TESSELATION
         )
    def print_landmarks(self, pos) :
          print("\n---Tracker---")
          for name, p in pos.items() :
                print(f"{name:<10} -> x: {p.x:.3f}  y: {p.y:.3f}  z: {p.z:.3f} ")
          print("\n----------")  

    def smoothed_points(new_point, old_point, alpha=0.2) :
          smoothed = {}
          for name, new_p in new_point.items(): 
                if old_point is None :
                      smoothed[name] = new_p
                else :
                      old_point = old_point[name]
                      smoothed[name] = point3D(
                            x = alpha * new_p + (1-alpha) * old_point, 
                            y = alpha * new_p + (1-alpha) * old_point, 
                            z = alpha * new_p + (1-alpha) * old_point
                      )

          return smoothed
    
    def pitch_vectors(self, smoothed_points) :
        nose = smoothed_points["Nose"]
        forehead = smoothed_points["Forehead"]
        chin = smoothed_points["Chin"]
        cheek = smoothed_points["Cheek"]

        pitch_vect = (chin.x - forehead.x, chin.y - forehead.y)
        yaw_vect = (-(nose.x - cheek.x), nose.y - cheek.y)
        roll_vect = (cheek.x - forehead.x, cheek.y - forehead.y)

        return { 
            "pitch_vect": pitch_vect,
            "yaw_vect": yaw_vect,
            "roll_vect": roll_vect
        }