import pygame

class SceneGen :
    def __init__(self): 
        pygame.init()
        self.W, self.H = 1280, 720 
        self.screen = pygame.display.set_mode((self.W, self.H))
        self.clock = pygame.time.Clock()


    def update(self, pitch, yaw, roll, pose) : 

        for event in pygame.event.get()  :
            if event.type == pygame.QUIT: 
                pygame.quit
                return False 
            

        self.screen.fill((15,15,18))


        pygame.display.flip()
        self.clock.tick(60)
        return True 
