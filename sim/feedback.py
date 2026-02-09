import time 

class feedBackEngine:   
    def __init__(self):
        self.last_pose = "FORWARD"
        self.pose_counter = 0
        self.confirmed_pose = "FORWARD"
    

    def assign_pose(self, pitch, yaw, roll) :

        if pitch > 12 :
            return "LOOKING DOWN"
     
        if yaw > 40 : 
            return "RIGHT BLINDSPOT"
        if yaw > 20: 
            return "RIGHT MIRROR"
        
        if yaw < -40 : 
            return "LEFT BLINDSPOT"
        if yaw < -20: 
            return "LEFT MIRROR"
        

        return "FORWARD"
        

    
    def update(self, pitch, yaw, roll) :
        pose = self.assign_pose(pitch, yaw, roll) 


        if pose == self.last_pose:
            self.pose_counter += 1
        else :
            self.pose_counter = 1

        self.last_pose = pose


        if self.pose_counter >= 5: 
            self.confirmed_pose = pose

        return self.confirmed_pose