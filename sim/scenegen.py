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
        image_path = os.path.join(base_directory, "Proto_images", "kloppenheim_06_4k.png")
        self.pano = pygame.image.load(image_path).convert()
        self.pano_width = self.pano.get_width()
        self.pano_height = self.pano.get_height()
        self.camera_x = 0
        self.camera_y = 0
        self.camera_initialized = False 
        
        self.state = "home"
        self.ui = None
    
    def handle_events(self) :
        for event in pygame.event.get()  :
            if event.type == pygame.QUIT: 
                pygame.quit()
                return False 
        return True 



    def update_homepage(self) :
        self.ui.draw_homepage()
        pygame.display.flip()
        self.clock.tick(self.fps)
        return True 

    
    def update(self, pitch=None, yaw=None, roll=None, pose=None, progress_data=None) :
        if not self.handle_events() :
            return False
        
        if self.state == "home": 
            return self.update_homepage()
        
        elif self.state == "simulation" :
            if pitch is None or yaw is None or roll is None or pose is None : 
                return True 
            return self.update_simulation(pitch, yaw, roll, pose, progress_data)
        
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

        
        
       

        pygame.display.flip()
        self.clock.tick(self.fps)
        return True 

