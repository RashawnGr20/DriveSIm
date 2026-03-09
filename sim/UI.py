import pygame 

class UI :
  
  def __init__(self, screen, screen_width, screen_height, ):
     
    self.W = screen_width
    self.H = screen_height
    self.screen = screen 
    self.panel_size = 150
    self. colors  = {
      
      "background": (18, 18, 22),
      "panel": (30, 30 ,40),
      "text": (230, 230, 235),
      "accent": (80, 150, 255),
      "sucess": (90, 200, 120),
      "warning": (230, 180, 80),
      "divider": (80, 80, 90)
    }
    
    self.fonts = {
      #"small": pygame.font.Font("fonts/inter.ttf", 16),
      #"medium": pygame.font.Font("fonts/inter.ttf", 22), 
      #"large": pygame.font.Font("fonts/inter.ttf", 32)
    
    }
    
    self.font_med = pygame.font.SysFont("Arial", 24)

  
  def draw(self, pose) :
    self.draw_running_ui(pose)
  
  
  def draw_tutorial(self) :
    pass
  
  
  def draw_running_ui(self, pose) :
    panel_color  = self.colors["panel"]
    text_color  = self.colors["text"]
    
    self.draw_bottom_panel(panel_color, pose, text_color)
  
  
  def draw_bottom_panel(self, panel_color, pose, text_color) :
    panel_y = self.H - self.panel_size
    pygame.draw.rect(
      self.screen, 
      panel_color,
      (0, panel_y, self.W, self.panel_size)
    )
  
    text_surface = self.font_med.render(f"POSE: {pose}", True, text_color,)
    self.screen.blit(text_surface, (20, panel_y + 20)) 
    
    pygame.draw.line(self.screen, (80,80,90), (0, panel_y), (self.W, panel_y), 2)
  
  
  def draw_progress(self) :
    pass 
  
  