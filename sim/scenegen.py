import pygame
import os

class SceneGen :
    def __init__(self, W, H , fps,): 
        pygame.init()
        self.W, self.H = W, H 
        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Test")
        self.clock = pygame.time.Clock()
        self.fps = fps 
        self.font = pygame.font.SysFont(None, 36)
        base_directory = os.path.dirname(__file__)
        image_path = os.path.join(base_directory, "Proto_images", "german_town_street_4k.png")
        self.pano = pygame.image.load(image_path).convert()
        self.pano_width = self.pano.get_width()
        self.pano_height = self.pano.get_height()
        self.camera_x = 0
        self.camera_y = 0
        self.camera_initialized = False 
        
        self.state = "home"
        self.ui = None
        self.selected_scene = None
        self.last_score = None 
        self.last_result = None


        self.click_to_state = {
            "start_session": "scene_select", 
            "select_scenario": "scene_select", 
            "about": "about", 
            "features": "features", 
            "scenarios": "scene_select", 
            "login": "auth", 
            "signup": "auth" 

        }

        self.auth_mode = "login"
        self.is_authenticated = False
        self.is_guest = False 
        self.pending_destination = False 

        self.scene_info = { 
            "left_lane_change": {
                "title": "Left Lane Change",
                "scenario_type": "Sequence",
                "description": "Check the required mirror and blind spot observations before lane movement. Order matters here.",
                "required_checks": ["TOP MIRROR", "LEFT MIRROR", "LEFT BLINDSPOT"],
               "image_key": "select_scene_2"
            },
            
            "4Way_left_turn": {
                "title": "Four-Way Left Turn",
                "scenario_type": "Coverage",
                "description": "Observe the key zones required for a safe left turn through the intersection.",
                "required_checks": ["FORWARD", "LEFT MIRROR", "RIGHT MIRROR"],
                "image_key": "select_scene_1"
        }
    }
        
        self.transition_alpha = 0
        self.is_fading_in = False
        self.fade_speed = 17

    def handle_events(self) :
        for event in pygame.event.get()  :
            if event.type == pygame.QUIT: 
                pygame.quit()
                return False 
        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                mouse_pos = event.pos

                if self.state == "home" and self.ui :
                    target = self.ui.get_home_click_target(mouse_pos)

                    if target == "login" :
                        self.auth_mode = "login"
                        self.state = "auth"
                        self.start_fade_in()
                    
                    elif target == "signup": 
                        self.auth_mode = "signup"
                        self.state = "auth"
                    
                    elif target in {"start_session", "select_scenario", "scenarios"} :
                        destination  = self.click_to_state[target]

                        if not self.is_authenticated : 
                            self.pending_destination = destination
                            self.auth_mode = "login"
                            self.state = "auth"
                        else  :
                            self.state = destination
                        
                        self.start_fade_in()
                    
                    elif target in self.click_to_state : 
                        self.state = self.click_to_state[target]
                        self.start_fade_in()

                elif self.state == "scene_select" and self.ui :
                    target = self.ui.get_scene_select_click_target(mouse_pos)

                    if target == "left_lane_change" :
                        self.selected_scene = "left_lane_change"
                        self.state = "scene_intro"
                        self.start_fade_in()
                    elif target == "four_way_left_turn":
                        self.selected_scene = "4Way_left_turn"
                        self.state = "scene_intro"
                        self.start_fade_in()

                    elif target == "coming_soon":
                        print("More scenarios coming soon.")
                elif self.state  == "scene_intro" and self.ui :
                    target = self.ui.get_scene_intro_click_target(mouse_pos)

                    if target == "start_simulation" :
                        self.state = "simulation"
                        self.start_fade_in()
                    elif target == "back_to_scenarios" :
                        self.state = "scene_select"
                        self.start_fade_in()
                
                elif self.state == "results" and self.ui :
                    target = self.ui.get_results_click_target(mouse_pos)

                    if target == "retry_scenario" :
                        self.state = "scene_intro"
                        self.start_fade_in()

                    elif target == "back_to_scenarios" :
                        self.state = "scene_select"
                        self.start_fade_in()
        return True 

    def start_fade_in(self) :
        self.transition_alpha = 220
        self.is_fading_in = True 
    
    def draw_fade_overlay(self):
        if not self.is_fading_in:
            return

        overlay = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        overlay.fill((18, 14, 13, self.transition_alpha))
        self.screen.blit(overlay, (0, 0))

        self.transition_alpha -= self.fade_speed
        if self.transition_alpha <= 0:
            self.transition_alpha = 0
            self.is_fading_in = False

    def update_homepage(self) :
        self.ui.draw_homepage()
        self.draw_fade_overlay()
        pygame.display.flip()
        self.clock.tick(self.fps)
        return True 

    def update_scene_select(self) :
        self.ui.draw_scene_select()
        self.draw_fade_overlay()
        pygame.display.flip()
        self.clock.tick(self.fps)
        return True 
    
    def update_scene_intro(self):
        scene_data = self.scene_info.get(self.selected_scene)
        self.ui.draw_scene_intro(scene_data)
        self.draw_fade_overlay()
        pygame.display.flip()
        self.clock.tick(self.fps)
        return True

    def update_results(self):
        scene_data = self.scene_info.get(self.selected_scene)
        self.ui.draw_results(scene_data, self.last_score, self.last_result)
        self.draw_fade_overlay()
        pygame.display.flip()
        self.clock.tick(self.fps)
        return True

    
    def update(self, pitch=None, yaw=None, roll=None, pose=None, progress_data=None) :
        if not self.handle_events() :
            return False
        
        if self.state == "home": 
            return self.update_homepage()
        
        elif self.state == "scene_select" :
            return self.update_scene_select()

        elif self.state == "scene_intro" :
            return self.update_scene_intro()
        
        elif self.state == "simulation" :
            if pitch is None or yaw is None or roll is None or pose is None : 
                return True 
            return self.update_simulation(pitch, yaw, roll, pose, progress_data)
        elif self.state == "results" :
            return self.update_results()
        
        return True 


    def update_simulation(self, pitch, yaw, roll, pose, progress_data=None) : 
        
        
        minYaw = -70
        maxYaw = 70
        minPitch = -20
        maxPitch = 20
        sensX = 1.6
        sensY = 1.4
        smoothing = 0.18
        pitch = max(minPitch, min(pitch, maxPitch)) * sensY
        yaw = max(minYaw, min(yaw, maxYaw)) * sensX 
        normx = (yaw - minYaw) / (maxYaw - minYaw)
        normy = (pitch - minPitch) / (maxPitch - minPitch)
        
        self.ui.draw_background_components()
        viewport = self.ui.viewport_rect 
        
        if self.camera_x == 0 and self.camera_y == 0:
            self.camera_x = (self.pano_width - viewport.w) // 2
            self.camera_y = (self.pano_height - viewport.h) // 2
            self.camera_initialized = True

        target_x = normx*(self.pano_width - viewport.w)
        target_y = normy*(self.pano_height - viewport.h)

        self.camera_x += (target_x - self.camera_x) * smoothing 
        self.camera_y += (target_y - self.camera_y) * smoothing

        x = max(0, min((self.pano_width - viewport.w), self.camera_x))
        y = max(0, min((self.pano_height - viewport.h), self.camera_y))

        viewport_surface = pygame.Surface((viewport.w, viewport.h), pygame.SRCALPHA)
        viewport_surface.blit(self.pano, (0, 0), (x, y, viewport.w, viewport.h))

        mask = pygame.Surface((viewport.w, viewport.h), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255,255,255,255), (0,0,viewport.w,viewport.h), border_radius=10)

        viewport_surface.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            
        self.screen.blit(viewport_surface, (viewport.x, viewport.y))

        self.ui.draw_overlay(pose, progress_data)

        
        
       
        self.draw_fade_overlay()
        pygame.display.flip()
        self.clock.tick(self.fps)
        return True 

    