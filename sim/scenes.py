from feedback import feedBackEngine

feedback = feedBackEngine()
class Scene :

    def __init__(self, scene_name):

        self.scenes = { 

            'left_lane_change' : SequenceScene(
                15,
                ['TOP MIRROR', 'LEFT MIRROR', 'LEFT BLINDSPOT'] 
            ),

            '4Way_left_turn' : coverageScene(
                15,
                ['FORWARD', 'LEFT MIRROR', 'RIGHT MIRROR']
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
        
    def get_progress_data(self) :
        if self.current_scene :
            return self.current_scene.get_progress_data()
        return None 
    
class SequenceScene :

        def __init__(self, min_glance, expected_sequence):
            self.expected_sequence = expected_sequence
            self.min_glance = min_glance 
            self.curr_step = 0
            self.step_lock = False
            self.last_pose = None

            self.step_results = ["pending"] * len(expected_sequence)
            self.observed_for_step = [None] * len(expected_sequence)

        def evaluate(self, pose, pose_counter) :

            if self.curr_step >= len(self.expected_sequence) :
                if self.curr_step >= len(self.expected_sequence) :
                    return {
                        "finished": True, 
                        "result": self.step_results, 
                        "reason": "completed"
                    } 
            
            expected_pose = self.expected_sequence[self.curr_step]
       
            if self.last_pose and pose != self.last_pose:
                self.step_lock = False 
        

            if pose_counter >= self.min_glance and not self.step_lock:
                if pose == expected_pose :
                    self.step_results[self.curr_step] = "correct"
                    self.observed_for_step[self.curr_step] = pose
                    self.curr_step += 1
                    self.step_lock = True 
                
                
        
                elif pose in self.expected_sequence and pose != expected_pose :
                    self.step_results[self.curr_step] = "missed"
                    self.observed_for_step[self.curr_step] = pose
                    self.curr_step += 1
                    self.step_lock = True
                
        
            self.last_pose = pose

            if self.curr_step >= len(self.expected_sequence) :
                if self.curr_step >= len(self.expected_sequence) :
                    return {
                        "finished": True, 
                        "result": self.step_results, 
                        "reason": "completed"
                    } 
                
            return None 
           
        
        def get_progress_data(self) :

            return {
                'type': "sequence",
                "expected": self.expected_sequence,
                "step_results": self.step_results,
                "observed_for_step": self.observed_for_step, 
                "current_index": self.curr_step

            }
        
        def get_outcome(self) :
           if self.curr_step >= len(self.expected_sequence) :
               return {
                   "finished": True, 
                   "result": self.step_results, 
                   "reason": "completed"
               } 
           
           return None 

    
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
                return {
                   "finished": True, 
                   "result": self.step_results, 
                   "reason": "completed"
               } 
            if self.last_pose and pose != self.last_pose:
                self.step_lock = False 
        
            if pose in self.required_zones and self.step_lock == False and pose_counter >= self.min_glance:
                self.checked_zones.add(pose)
                self.step_lock = True
            else :
                return None 
            
            self.last_pose = pose


            if self.checked_zones == self.required_zones :
                return {
                   "finished": True, 
                   "result": self.step_results, 
                   "reason": "completed"
               } 
            
            return None 
    
        def get_progress_data(self) :
            return {
                'type': "coverage",
                "expected": list(self.expected_sequence),
                "completed": list(self.checked_zones),
                "current_index": None

            }
        
    


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
            
    
    
    def sequence_score(self, step_results) :

        correct = sum(1 for result in step_results if result == "correct")
        return (correct / len(self.expected_sequence)) * 100 

            
        
        
        
        
        


            



         



        







        




