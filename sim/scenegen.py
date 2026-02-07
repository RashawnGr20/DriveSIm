import pygame

class SceneGen :
    def __init__(self, W = 1280, H = 720, fps= 60): 
        pygame.init()
        self.W, self.H = W, H 
        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Test")
        self.clock = pygame.time.Clock()
        self.fps = fps 
        self.font = pygame.font.SysFont(None, 36)


    def update(self, pitch, yaw, roll, pose) : 

        for event in pygame.event.get()  :
            if event.type == pygame.QUIT: 
                pygame.quit()
                return False 
            

        self.screen.fill((15,15,18))

        text = F"Pitch {pitch:.2f} | Yaw {yaw:.2f} | Roll {roll:.2f} | {pose}"
        surf = self.font.render(text, True, (240, 240, 240))
        self.screen.blit(surf, (20,30))
        

        pygame.display.flip()
        self.clock.tick(self.fps)
        return True 

