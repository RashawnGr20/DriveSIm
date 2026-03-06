import pygame
import os

class SceneGen :
    def __init__(self, W = 1280, H = 720, fps= 60,): 
        pygame.init()
        self.W, self.H = W, H 
        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Test")
        self.clock = pygame.time.Clock()
        self.fps = fps 
        self.font = pygame.font.SysFont(None, 36)
        base_directory = os.path.dirname(__file__)
        image_path = os.path.join(base_directory, "Proto_images", "urban_street_01_4k.png")
        self.pano = pygame.image.load(image_path).convert()
        self.pano_width = self.pano.get_width()
        self.pano_height = self.pano.get_height()

        self.camera_x = (self.pano_width - self.W) // 2
        self.camera_y = (self.pano_height - self.H) // 2

    def update(self, pitch, yaw, roll, pose) : 

        for event in pygame.event.get()  :
            if event.type == pygame.QUIT: 
                pygame.quit()
                return False 
            

        self.screen.fill((15,15,18))

        text = F"Pitch {pitch:.2f} | Yaw {yaw:.2f} | Roll {roll:.2f} | {pose}"
        surf = self.font.render(text, True, (240, 240, 240))
        self.screen.blit(surf, (20,30))
        
        minYaw = -70
        maxYaw = 70
        minPitch = -20
        maxPitch = 20
        sensX = 2.5
        sensY = 0.3
        smoothing = 0.18
        pitch = max(minPitch, min(pitch, maxPitch)) * sensY
        yaw = max(minYaw, min(yaw, maxYaw)) * sensX 
        normx = (yaw - minYaw) / (maxYaw - minYaw)
        normy = (pitch - minPitch) / (maxPitch - minPitch)
        
        target_x = normx*(self.pano_width - self.W)
        target_y = normy*(self.pano_height - self.H)

        self.camera_x += (target_x - self.camera_x) * smoothing 
        self.camera_y += (target_y - self.camera_y) * smoothing

        x = max(0, min((self.pano_width - self.W), self.camera_x))
        y = max(0, min((self.pano_height - self.H), self.camera_y))
        self.screen.blit(self.pano, (0,0), (x, y, self.W, self.H))

        
       

        pygame.display.flip()
        self.clock.tick(self.fps)
        return True 

