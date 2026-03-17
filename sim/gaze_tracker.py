from feedback import feedBackEngine

feedback = feedBackEngine()

class gaze : 

    def __init__(self):
        
        self.last_pose = None 
        self.pose_counter = 0
    

    def gaze_estimation(self, pitch, yaw, pose, fps) :

        event_data = None 
        
        if self.last_pose is None :
            self.last_pose = pose
            self.pose_counter = 1
            return None 


        if pose == self.last_pose :
            self.pose_counter += 1

        else : 
            duration = self.pose_counter / fps

            event_data = {
                "pose": self.last_pose,
                "duration": duration

            }
        
            self.last_pose = pose
            self.pose_counter = 1

        return event_data
    
