import mediapipe as mp
import cv2
from collections import namedtuple
import math

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

      def get_gaze_pos(self, face_landmarks) : 
            
            left_eye  = {
                 "iris": [face_landmarks.landmark[474],face_landmarks.landmark[475],face_landmarks.landmark[476],face_landmarks.landmark[477]],
                  "outer": face_landmarks.landmark[33],
                  "inner": face_landmarks.landmark[133], 
                  "top": face_landmarks.landmark[159],
                  "bottom": face_landmarks.landmark[145]
            }

            right_eye = {
                  "iris": [face_landmarks.landmark[469],face_landmarks.landmark[470],face_landmarks.landmark[471],face_landmarks.landmark[472]], 
                  "outer": face_landmarks.landmark[362], 
                  "inner": face_landmarks.landmark[263], 
                  "top": face_landmarks.landmark[386], 
                  "bottom": face_landmarks.landmark[374]
            }

            return {
            "left_eye":{
                  "iris": [point3D(face_landmarks.landmark[i].x, face_landmarks.landmark[i].y, face_landmarks.landmark[i].z )
                           for i in [474, 475, 476, 477]
                           ],
                  "outer": point3D(left_eye["outer"].x, left_eye["outer"].y, left_eye["outer"].z),
                  "inner": point3D(left_eye["inner"].x,left_eye["inner"].y,left_eye["inner"].z), 
                  "top": point3D(left_eye["top"].x,left_eye["top"].y,left_eye["top"].z), 
                  "bottom": point3D(left_eye["bottom"].x,left_eye["bottom"].y,left_eye["bottom"].z), 
            },

            "right_eye": {
                  "iris": [point3D(face_landmarks.landmark[i].x, face_landmarks.landmark[i].y, face_landmarks.landmark[i].z )
                           for i in [469, 470, 471, 472]
                           ],
                  "outer": point3D(right_eye["outer"].x, right_eye["outer"].y, right_eye["outer"].z),
                  "inner": point3D(right_eye["inner"].x,right_eye["inner"].y,right_eye["inner"].z), 
                  "top": point3D(right_eye["top"].x,right_eye["top"].y,right_eye["top"].z), 
                  "bottom": point3D(right_eye["bottom"].x,right_eye["bottom"].y,right_eye["bottom"].z), 
                  }
            }

                
      def gaze_vectors(self) : 
           
           pass 

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

      def smoothed_points(self, new_point, old_point, alpha=0.2) :
          smoothed = {}
          for name, new_p in new_point.items(): 
                if old_point is None :
                      smoothed[name] = new_p
                else :
                      old_p = old_point[name]
                      smoothed[name] = point3D(
                            x = alpha * new_p.x + (1-alpha) * old_p.x, 
                            y = alpha * new_p.y + (1-alpha) * old_p.y, 
                            z = alpha * new_p.z + (1-alpha) * old_p.z
                      )

          return smoothed
    
      def wrap_deg(self, a) :
          
          while a > 180 :
                a -= 360
          while a < -180 :
                a+= 360
          return a 
    
    
      def pitch_vectors(self, smoothed_points) :
            nose = smoothed_points["Nose"]
            forehead = smoothed_points["Forehead"]
            chin = smoothed_points["Chin"]
            cheek = smoothed_points["Cheek"]

            dy_pitch = chin.y - forehead.y
            dz_pitch = chin.z - forehead.z

            

            dx_yaw = nose.x - cheek.x
            dz_yaw = nose.z - cheek.z
            roll_vectx = (cheek.x - forehead.x) 
            roll_vecty = (cheek.y - forehead.y)

            yaw_angle = self.wrap_deg(math.atan2(dx_yaw, dz_yaw)*(180/math.pi))
            roll_angle = self.wrap_deg(math.atan2(roll_vecty, roll_vectx)*(180/math.pi))
            pitch_angle = self.wrap_deg(math.atan2(dz_pitch, dy_pitch) * (180/math.pi))

            return { 
                  "pitch_angle": pitch_angle,
                  "yaw_angle": yaw_angle,
                  "roll_angle": roll_angle
            }
      
  