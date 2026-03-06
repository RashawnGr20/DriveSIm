from feedback import feedBackEngine

feedback = feedBackEngine()
class scene :

    def __init__(self, scenes, sequence, min_glance):

        self.scenes = { 

            'left_lane_change' :  {
                'sequence': ['TOP MIRROR', 'LEFT MIRROR', 'LEFT BLINDSPOT'], 
                'min_glance':  10
            },

            'right_lane_change': { 
                
                'sequence': ['TOP MIRROR', 'RIGHT MIRROR', 'RIGHT BLINDSPOT'], 
                'min_glance': 8                  
            
            }

        }

        self.curr_step = 0
        self.last_pose_counter = 0
        self.last_pose = None
        self.step_lock = False 
        self.glance_data = []

    def evaluation(self, selected_scene, pose_counter, fps, pose) :
        
        scene = self.scenes[selected_scene]
        expected_sequence = scene['sequence']
        min_glance = scene['min_glance']
        
        
        
        if self.curr_step >= len(expected_sequence) :
            pass 
        else :
            expected_pose = expected_sequence[self.curr_step]
        
        if self.last_pose and pose != self.last_pose:
            duration_frames = self.last_pose_counter
            duration_seconds = duration_frames / fps
            self.glance_data.append((self.last_pose, duration_seconds))
            self.step_lock = False

        if pose == expected_pose and pose_counter >= min_glance and self.step_lock == False:
            self.curr_step += 1
            self.step_lock = True 
        
        elif pose in expected_sequence and pose != expected_pose and pose_counter >= min_glance :
            self.curr_step = 0
        
        else : 
            pass 

        self.last_pose = pose
        self.last_pose_counter = pose_counter



        







        




