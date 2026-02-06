import time 

class feedBackEngine:   
    def __init__(self):
        self.last_pose = "FORWARD"
        self.pose_counter = 0
        self.confirmed_pose = "FORWARD"
    

    def assign_pose(self, pitch, yaw, roll) :

        if pitch > 10 :
            return "LOOKING DOWN"
        elif yaw < -20 : 
            return "RIGHT BLINDSPOT"
        elif yaw > 5 :
            return "LEFT MIRROR" 
        elif yaw < -5 :
            return "RIGHT MIRROR"
        elif yaw > 20 :
            return "LEFT BLINDSPOT"
        else :
            return "FORWARD"
        

    
    def update(self, pitch, yaw, roll) :
        pose = self.assign_pose(pitch, yaw, roll) 


        if pose == self.last_pose:
            self.pose_counter += 1
        else :
            self.pose_counter = 0

        self.last_pose = pose


        if self.pose_counter >= 5: 
            self.confirmed_pose = pose

        return self.confirmed_pose