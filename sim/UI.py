import pygame 
import os 

class UI :
  
  def __init__(self, screen, screen_width, screen_height, ):
    
    
    base_dir = os.path.dirname(__file__)
    
    small_font_path = os.path.join(base_dir, "fonts", "Inter_18pt-ExtraLight.ttf")
    
    large_font_path = os.path.join(base_dir, "fonts", "Inter_28pt-SemiBold.ttf")
     
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
      "small": pygame.font.Font(small_font_path, 16),
      "medium": pygame.font.Font(small_font_path, 22), 
      "large": pygame.font.Font(large_font_path, 32)
  
    }

  
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
    
    panel_surface = pygame.Surface((self.W, self.panel_size), pygame.SRCALPHA)
    panel_surface.set_alpha(230)
    panel_surface.fill(panel_color)
    
    self.screen.blit(panel_surface, (0, panel_y))
    
    pygame.draw.line(
      self.screen, 
      self.colors["divider"],
      (250, panel_y + 10),
      (250, panel_y + self.H - 10),
      1
    )
    
    pygame.draw.line(
      self.screen, 
      self.colors["accent"], 
      (0, panel_y),
      (self.W, panel_y),
      2
    )
    
    label = self.fonts["small"].render("CURRENT POSE", True, self.colors['divider'])
    self.screen.blit(label, (20, panel_y + 10)) 
    
    pose_text = self.fonts["large"].render(pose, True, self.colors["accent"])
    self.screen.blit(pose_text, (20, panel_y + 40))
    
  
    progress_label = self.fonts["small"].render(
      "OBSERVATIONS PROGRESS", 
      True,
      self.colors["divider"]
    )
    
    self.screen.blit(progress_label, (270, panel_y + 10))
    
    
  
  def draw_progress(self) :
    pass 
  
  