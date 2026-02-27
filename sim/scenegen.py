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
        image_path = os.path.join(base_directory, "Proto_images", "wide_street_01_4k.png")
        self.pano = pygame.image.load(image_path).convert()
        self.pano_width = self.pano.get_width()
        self.pano_height = self.pano.get_height()

    def update(self, pitch, yaw, roll, pose) : 

        for event in pygame.event.get()  :
            if event.type == pygame.QUIT: 
                pygame.quit()
                return False 
            

        self.screen.fill((15,15,18))

        text = F"Pitch {pitch:.2f} | Yaw {yaw:.2f} | Roll {roll:.2f} | {pose}"
        surf = self.font.render(text, True, (240, 240, 240))
        self.screen.blit(surf, (20,30))
        
        minYaw = -60
        maxYaw = 60
        minPitch = -15
        maxPitch = 15
        pitch = max(minPitch, min(pitch, maxPitch))
        yaw = max(minYaw, min(yaw, maxYaw))
        normx = (yaw - minYaw) / (maxYaw - minYaw)
        normy = (pitch - minPitch) / (maxPitch - minPitch)
        cam_x = normx*(self.pano_width - self.W)
        cam_y = normy*(self.pano_height - self.H)

        x = max(0, min((self.pano_width - self.W), cam_x))
        y = max(0, min((self.pano_height - self.H) * 0.4, cam_y))
        self.screen.blit(self.pano, (0,0), (x, y, self.W, self.H))

        
       

        pygame.display.flip()
        self.clock.tick(self.fps)
        return True 

