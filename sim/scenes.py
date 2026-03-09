from feedback import feedBackEngine

feedback = feedBackEngine()
class Scene :

    def __init__(self, scene_name):

        self.scenes = { 

            'left_lane_change' : SequenceScene(
                10,
                ['TOP MIRROR', 'LEFT MIRROR', 'LEFT BLINDSPOT'] 
            ),

            '4Way_left_turn' : coverageScene(
                10,
                ['FORWARD', 'LEFT-MIRROR', 'RIGHT-MIRROR']
            )
        }

        self.current_scene = self.get_scene(scene_name)
        
    def get_scene(self, selected_scene) :
         
        if selected_scene in self.scenes :
            return self.scenes[selected_scene]
        else :
             print('Scene does not exist') 
             return None


    
    def evaluation(self, pose_counter, pose) :         
        
        return self.current_scene.evaluate(pose, pose_counter)
        
    
    
class SequenceScene :

        def __init__(self, min_glance, expected_sequence):
            self.expected_sequence = expected_sequence
            self.min_glance = min_glance 
            self.curr_step = 0
            self.observations = []
            self.step_lock = False
            self.last_pose = None

        def evaluate(self, pose, pose_counter) :

            if self.curr_step >= len(self.expected_sequence) :
                    return self.observations
            else :
                expected_pose = self.expected_sequence[self.curr_step]
       
            if self.last_pose and pose != self.last_pose:
                self.step_lock = False 
        

            if pose == expected_pose and pose_counter >= self.min_glance and self.step_lock == False:
                self.curr_step += 1
                self.step_lock = True
                self.observations.append(pose) 
        
            elif pose in self.expected_sequence and pose != expected_pose and pose_counter >= self.min_glance and self.step_lock == False :
                self.curr_step += 1
                self.observations.append(pose)
        
            else : 
                pass 

            self.last_pose = pose

    
class coverageScene :

        def __init__(self, min_glance, expected_sequence):
            
            self.expected_sequence = expected_sequence
            self.min_glance = min_glance 
            self.required_zones = set(expected_sequence)
            self.checked_zones = set()
            self.step_lock = False
            self.last_pose = None
        
        def evaluate(self, pose, pose_counter) :


            if self.checked_zones == self.required_zones :
                return self.checked_zones 
            
            if self.last_pose and pose != self.last_pose:
                self.step_lock = False 
        
            if pose in self.required_zones and self.step_lock == False and pose_counter >= self.min_glance:
                self.checked_zones.add(pose)
                self.step_lock = True
            else :
                return None 
            
            self.last_pose = pose


            return self.checked_zones
            


class Metrics :
    
    def __init__(self, expected_sequence):
        
        self.last_pose = None 
        self.pose_counter = 0 
        self.expected_sequence = expected_sequence
        self.glance_data = []
    
    
    def record_glance(self, fps, pose) :
        
        if pose != self.last_pose :
            duration = self.pose_counter / fps
            self.glance_data.append((self.last_pose, duration))
            
        self.last_pose = pose
            
    
    
    def sequence_score(self, observations) :

        score = 0 
        for i in range(min(len(self.expected_sequence), len(observations))) :
            
            if observations[i] == self.expected_sequence[i] :
                score += 1
            
        return (score / len(self.expected_sequence)) * 100

            
        
        
        
        
        


            



         



        







        




