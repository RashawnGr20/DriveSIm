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

            self.GAZE_BASELINE_FRAMES = 50

            self.eye_height_ref = {"left": None, "right": None}
            self.eye_height_buffer = {"left": [], "right": []}
            
            
            
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
            self.eye_height_ref = {"left": None, "right": None}
            self.eye_height_buffer = {"left": [], "right": []}

      def collect_gaze_ref(self, buffer_name, left_height, right_height):
            if buffer_name == "center_ref" :
                  self.eye_height_buffer["left"].append(left_height)
                  self.eye_height_buffer["right"].append(right_height)
                  return len(self.eye_height_buffer["left"]) >= self.GAZE_BASELINE_FRAMES

      def finalize_center_ref(self) :
            
            if not self.eye_height_buffer["left"] or not self.eye_height_buffer["right"] : 
                  return False 
            
            self.eye_height_ref["left"] = sum(self.eye_height_buffer["left"]) / len(self.eye_height_buffer["left"])
            self.eye_height_ref["right"] = sum(self.eye_height_buffer["right"]) / len(self.eye_height_buffer["right"])
            
      
            self.eye_height_buffer["right"].clear()
            self.eye_height_buffer["left"].clear()
            return True 
      
      def compute_eye_height(self, eye_data) :
            top = eye_data["top"]
            bottom = eye_data["bottom"]

            return math.sqrt((bottom.x - top.x) **2 + (bottom.y - top.y) ** 2)

      def compute_iris_center(self, iris_points) :
            x = sum(p.x for p in iris_points) / len(iris_points)
            y = sum(p.y for p in iris_points) / len(iris_points) 
            return point3D(x, y, 0.0)
      

      def compute_eye_center(self, eye_data) : 
            inner = eye_data["inner"]
            outer = eye_data["outer"]
            top = eye_data["top"]
            bottom = eye_data["bottom"] 


            corner_mid_x = (inner.x + outer.x) / 2
            corner_mid_y= (inner.y + outer.y) / 2

            lid_mid_y = (top.y + bottom.y) / 2

            center_x = corner_mid_x

            center_y = 0.5  * corner_mid_y + 0.5 * lid_mid_y

            return point3D(center_x, center_y, 0.0)

            

      def compute_eye_axes(self, eye_data) : 
            p1 = eye_data["inner"]
            p2 = eye_data["outer"]

            if p1.x <= p2.x : 
                  left_corner = p1
                  right_corner = p2
            else : 
                  left_corner = p2
                  right_corner = p1

            vx = right_corner.x - left_corner.x
            vy = right_corner.y - left_corner.y
            
            length = math.sqrt(vx**2 + vy**2)
            eps = 1e-6

            eye_x_unit = (vx / max(length, eps), vy / max(length, eps))
            eye_y_unit = (-eye_x_unit[1], eye_x_unit[0])

            return eye_x_unit, eye_y_unit

      def project_to_eye_frame(self, iris_center, eye_center, eye_x_unit, eye_y_unit) : 
            dx = iris_center.x - eye_center.x
            dy = iris_center.y - eye_center.y

            local_x = dx * eye_x_unit[0] + dy * eye_x_unit[1]
            local_y = dx * eye_y_unit[0] + dy * eye_y_unit[1]

            return local_x, local_y

      def compute_eye_scale(self, eye_data) : 
            inner = eye_data["inner"]
            outer = eye_data["outer"]
            top = eye_data["top"]
            bottom = eye_data["bottom"]

            eye_width = math.sqrt((outer.x - inner.x)**2 + (outer.y - inner.y)**2)
            eye_height = math.sqrt((bottom.x - top.x)**2 + (bottom.y - top.y)**2)

            eps = 1e-6
            return max(eye_width, eps), max(eye_height, eps)



      def compute_eye_gaze(self, eye_data, eye_name) : 
            iris_center = self.compute_iris_center(eye_data["iris"])
            eye_center = self.compute_eye_center(eye_data)
            eye_x_unit, eye_y_unit = self.compute_eye_axes(eye_data)

            local_x, local_y = self.project_to_eye_frame(iris_center, eye_center, eye_x_unit, eye_y_unit)

            eye_width, live_eye_height = self.compute_eye_scale(eye_data)

            ref_eye_height = self.eye_height_ref[eye_name]
            effective_eye_height = ref_eye_height if ref_eye_height is not None else live_eye_height
            
            norm_x = local_x / (eye_width / 2)
            norm_y = local_y / (effective_eye_height / 2)
            
            if ref_eye_height is None  or ref_eye_height <1e-6: 
                  eye_openess_delta = 0.0 
            else :
                  eye_openess_delta = (live_eye_height - ref_eye_height) / ref_eye_height
                  
            k = 0.30
            s = 2.0 
            compresed_openess = math.tanh(s * eye_openess_delta)
            vertical_blend = norm_y - k * compresed_openess
            
            print("eye:", eye_name)
            print("local_y:", local_y)
            print("norm_y:", norm_y)
            print("live_eye_height:", live_eye_height)
            print("ref_eye_height:", ref_eye_height)
            print("openness_delta:", eye_openess_delta)
            
            return norm_x, vertical_blend

      def normalized_gaze(self, face_landmarks) : 
            eye_data  = self.get_gaze_pos(face_landmarks)

            left_x, left_y = self.compute_eye_gaze(eye_data["left_eye"], "left") 
            right_x, right_y = self.compute_eye_gaze(eye_data["right_eye"], "right")

            norm_x = (left_x + right_x) / 2
            norm_y = (left_y + right_y) / 2

            print("left local gaze:", left_x, left_y)
            print("right local gaze:", right_x, right_y)
            print("avg local gaze:", norm_x, norm_y)

            return norm_x, norm_y
            

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
      
  