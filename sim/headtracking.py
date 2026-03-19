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

            self.prev_gaze = None 
            self.gaze_baseline = None 
            self.gaze_baseline_buffer = []
            self.GAZE_BASELINE_FRAMES = 50

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

      def get_gaze_pos(self, face_landmarks):

            left_eye = {
                  "iris": [
                        face_landmarks.landmark[469],
                        face_landmarks.landmark[470],
                        face_landmarks.landmark[471],
                        face_landmarks.landmark[472]
                  ],
                  "outer": face_landmarks.landmark[33],
                  "inner": face_landmarks.landmark[133],
                  "top": face_landmarks.landmark[159],
                  "bottom": face_landmarks.landmark[145]
            }

            right_eye = {
                  "iris": [
                        face_landmarks.landmark[474],
                        face_landmarks.landmark[475],
                        face_landmarks.landmark[476],
                        face_landmarks.landmark[477]
                  ],
                  "outer": face_landmarks.landmark[362],
                  "inner": face_landmarks.landmark[263],
                  "top": face_landmarks.landmark[386],
                  "bottom": face_landmarks.landmark[374]
            }

            return {
                  "left_eye": {
                        "iris": [
                              point3D(p.x, p.y, p.z) for p in left_eye["iris"]
                        ],
                        "outer": point3D(left_eye["outer"].x, left_eye["outer"].y, left_eye["outer"].z),
                        "inner": point3D(left_eye["inner"].x, left_eye["inner"].y, left_eye["inner"].z),
                        "top": point3D(left_eye["top"].x, left_eye["top"].y, left_eye["top"].z),
                        "bottom": point3D(left_eye["bottom"].x, left_eye["bottom"].y, left_eye["bottom"].z),
                  },

                  "right_eye": {
                        "iris": [
                              point3D(p.x, p.y, p.z) for p in right_eye["iris"]
                        ],
                        "outer": point3D(right_eye["outer"].x, right_eye["outer"].y, right_eye["outer"].z),
                        "inner": point3D(right_eye["inner"].x, right_eye["inner"].y, right_eye["inner"].z),
                        "top": point3D(right_eye["top"].x, right_eye["top"].y, right_eye["top"].z),
                        "bottom": point3D(right_eye["bottom"].x, right_eye["bottom"].y, right_eye["bottom"].z),
                  }
            }

      def reset_gaze(self) :
            self.prev_gaze = None
            self.gaze_baseline = None
            self.gaze_baseline_buffer = []
                
      def gaze_vectors(self, norm_x, norm_y) :  
            
            if self.gaze_baseline is None :
                  return 0.0, 0.0
            
            baseline_x, baseline_y = self.gaze_baseline

            print("delta:", norm_x - baseline_x, norm_y - baseline_y)

            offset_x = (norm_x - baseline_x) / 0.07
            offset_y = (norm_y - baseline_y) / 0.06

            gain = 1.0
            offset_x *= gain
            offset_y *= gain

            offset_x = max(-1, min(1, offset_x))
            offset_y = max(-1, min(1, offset_y))

            offset_x = -offset_x
            offset_y = -offset_y

            print("raw offset:", offset_x, offset_y)

            if self.prev_gaze is None : 
                  smoothed_x = offset_x
                  smoothed_y = offset_y
            else : 
                  prev_x, prev_y = self.prev_gaze

                  smoothed_x = self.smoothed_gaze(prev_x, offset_x)
                  smoothed_y = self.smoothed_gaze(prev_y, offset_y)

            self.prev_gaze = (smoothed_x, smoothed_y)

            print("smoothed offset:", smoothed_x, smoothed_y)

            return smoothed_x, smoothed_y
      


      def update_gaze_baseline(self, norm_x, norm_y) : 
            self.gaze_baseline_buffer.append((norm_x, norm_y))

            if len(self.gaze_baseline_buffer) < self.GAZE_BASELINE_FRAMES :
                  print("baseline sample:", norm_x, norm_y)
                  print("baseline buffer size:", len(self.gaze_baseline_buffer)) 
                  return False 

                  
            baseline_x = sum(x for x, y in self.gaze_baseline_buffer) / len(self.gaze_baseline_buffer)
            baseline_y = sum(y for x, y in self.gaze_baseline_buffer) / len(self.gaze_baseline_buffer)
            
            self.gaze_baseline = (baseline_x, baseline_y)
            print("FINAL BASELINE:", self.gaze_baseline)
            self.gaze_baseline_buffer.clear()
            return True 


      def normalized_gaze(self, face_landmarks) : 

            eye_data = self.get_gaze_pos(face_landmarks)

            left_iris = eye_data["left_eye"]["iris"]
            right_iris = eye_data["right_eye"]["iris"]

            shrink_factor = 1
            eps = 1e-6
            xL_avg = sum(p.x for p in left_iris) / len(left_iris)
            yL_avg = sum(p.y for p in left_iris) / len(left_iris) 
            zL_avg = sum(p.z for p in left_iris) / len(left_iris)

            xR_avg = sum(p.x for p in right_iris) / len(right_iris)
            yR_avg = sum(p.y for p in right_iris) / len(right_iris) 
            zR_avg = sum(p.z for p in right_iris) / len(right_iris)

            left_eye = eye_data["left_eye"]
            right_eye = eye_data["right_eye"]

            left_eye_left_bound = min(left_eye["outer"].x, left_eye["inner"].x)
            left_eye_right_bound = max(left_eye["outer"].x, left_eye["inner"].x)

            right_eye_left_bound = min(right_eye["outer"].x, right_eye["inner"].x)
            right_eye_right_bound = max(right_eye["outer"].x, right_eye["inner"].x)

            left_eye_upper_bound = min(left_eye["top"].y, left_eye["bottom"].y)
            left_eye_lower_bound = max(left_eye["top"].y, left_eye["bottom"].y)

            right_eye_upper_bound = min(right_eye["top"].y, right_eye["bottom"].y)
            right_eye_lower_bound = max(right_eye["top"].y, right_eye["bottom"].y)

            center_x_L = (left_eye_left_bound + left_eye_right_bound) / 2
            center_y_L = (left_eye_upper_bound + left_eye_lower_bound) / 2

            range_x_L = (left_eye_right_bound - left_eye_left_bound) * shrink_factor
            range_y_L = (left_eye_lower_bound - left_eye_upper_bound) * shrink_factor

            left_eye_left_bound  = center_x_L - range_x_L / 2
            left_eye_right_bound = center_x_L + range_x_L / 2

            left_eye_upper_bound = center_y_L - range_y_L / 2
            left_eye_lower_bound = center_y_L + range_y_L / 2

            center_x_R = (right_eye_left_bound + right_eye_right_bound) / 2
            center_y_R = (right_eye_upper_bound + right_eye_lower_bound) / 2

            range_x_R = (right_eye_right_bound - right_eye_left_bound)* shrink_factor
            range_y_R = (right_eye_lower_bound - right_eye_upper_bound)* shrink_factor

            right_eye_left_bound  = center_x_R - range_x_R / 2
            right_eye_right_bound = center_x_R + range_x_R / 2

            right_eye_upper_bound = center_y_R - range_y_R / 2
            right_eye_lower_bound = center_y_R + range_y_R / 2

            norm_x_l = (xL_avg - left_eye_left_bound) / max(eps, (left_eye_right_bound - left_eye_left_bound))
            norm_y_l = (yL_avg - left_eye_upper_bound) / max(eps, (left_eye_lower_bound - left_eye_upper_bound))

            norm_x_r = (xR_avg - right_eye_left_bound) / max(eps, (right_eye_right_bound - right_eye_left_bound))
            norm_y_r = (yR_avg - right_eye_upper_bound) / max(eps, (right_eye_lower_bound - right_eye_upper_bound))

            norm_x = (norm_x_l + norm_x_r) / 2
            norm_y = (norm_y_l + norm_y_r) / 2

            norm_x = max(0, min(1, norm_x))
            norm_y = max(0, min(1, norm_y))

            print("xL_avg, yL_avg:", xL_avg, yL_avg)
            print("xR_avg, yR_avg:", xR_avg, yR_avg)

            print("L bounds:", left_eye_left_bound, left_eye_right_bound, left_eye_upper_bound, left_eye_lower_bound)
            print("R bounds:", right_eye_left_bound, right_eye_right_bound, right_eye_upper_bound, right_eye_lower_bound)

            print("norm L:", norm_x_l, norm_y_l)
            print("norm R:", norm_x_r, norm_y_r)
            print("norm avg:", norm_x, norm_y)

            return norm_x, norm_y

      def smoothed_gaze(self, prev, offset, alpha=0.2) : 
            if prev is None : 
                  return offset 
            
            smoothed = prev + alpha *(offset - prev)

            return smoothed

            
            

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
      
  