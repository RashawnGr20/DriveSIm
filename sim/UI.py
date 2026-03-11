import pygame 
import os 

class UI :
  
    def __init__(self, screen, screen_width, screen_height, ):
    
    
        base_dir = os.path.dirname(__file__)
        
        small_font_path = os.path.join(base_dir, "fonts", "Nunito-Regular.ttf")
        
        large_font_path = os.path.join(base_dir, "fonts", "Nunito-SemiBold.ttf")
        
        self.W = screen_width
        self.H = screen_height
        self.screen = screen 
        self.panel_size = 150
        self. colors  = {
        
        "background": (24, 19, 18),
        "panel": (30, 30 ,40),
        "text": (230, 230, 235),
        "accent": (80, 150, 255),
        "success": (90, 200, 120),
        "warning": (230, 180, 80),
        "divider": (80, 80, 90), 
        "top_grad": (35, 28, 25),
        "bottom_grad": (14, 11, 10), 
        "card_shadow": (7,10,18),  
        "card_outer": (34, 41, 63),
        "card_inner": (19, 26, 42),
        "card_border": (56, 68, 102),
        "muted": (130, 145, 170),
        "chip": (42, 56, 88)
        }
        
        self.fonts = {
        "small": pygame.font.Font(small_font_path, 16),
        "medium": pygame.font.Font(small_font_path, 22), 
        "large": pygame.font.Font(large_font_path, 32)
    
        }

        margin = 24
        gap = 16
        bottom_cards_height = 220

        shell_x = margin
        shell_y = margin
        shell_w = self.W - 2*margin
        shell_h = self.H - 2*margin - gap - bottom_cards_height

        inner_pad = 7

        inner_x = shell_x + inner_pad
        inner_y = shell_y + inner_pad
        inner_w = shell_w - 2 * inner_pad
        inner_h = shell_h - 2 * inner_pad


        self.viewport_rect = pygame.Rect(inner_x, inner_y, inner_w, inner_h)

  
    def draw_background_components(self) :
    
      self.draw_background()
      self.draw_vertical_gradient()
      self.draw_view_shell()
      
  
    def draw_background(self) :
      self.screen.fill(self.colors["background"])

    def draw_overlay(self, pose, progress_data=None) :
      self.draw_smaller_cards(pose,progress_data)
      

    def draw_vertical_gradient(self) :
      top = self.colors["top_grad"]
      bottom = self.colors["bottom_grad"]


      for y in range(self.H) :
        t = y / ( self.H - 1)

         
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        
        pygame.draw.line(self.screen, (r, g, b), (0, y), (self.W - 1, y ))
  
    def draw_view_shell(self) :

        rect = self.viewport_rect

        pygame.draw.rect(
            self.screen,
            (42, 34, 31), 
            rect.inflate(14,14),
            border_radius=12
        )


        pygame.draw.rect(
            self.screen,
            (22,30,48),
            rect,
            border_radius=10
        )



    def draw_mini_bars(self, rect, values, color):
        bar_w = 10
        gap = 6
        base_y = rect.bottom - 24
        start_x = rect.x + 16

        for i, v in enumerate(values):
            h = max(6, int(v))
            bar_rect = pygame.Rect(start_x + i * (bar_w + gap), base_y - h, bar_w, h)
            pygame.draw.rect(self.screen, color, bar_rect, border_radius=3)

    def draw_smaller_cards(self, pose, progress_data=None):
        margin = 24
        gap = 30
        row_inset = 0
        card_h = 215
        row_x = margin + row_inset
        row_y = self.H - margin - card_h
        row_w = self.W - 2 * (margin + row_inset)

        card_w = (row_w - 2 * gap) // 3

        card1 = pygame.Rect(row_x, row_y, card_w, card_h)
        card2 = pygame.Rect(row_x + card_w + gap, row_y, card_w, card_h)
        card3 = pygame.Rect(row_x + 2 * (card_w + gap), row_y, card_w, card_h)

        self.draw_checklist_card(card1, "Current Posistion", pose, progress_data, self.colors["accent"])
        self.draw_soft_card(card2, "Scan Rate", "12/min", "Last 30 seconds", self.colors["success"])
        self.draw_soft_card(card3, "Hazard Checks", "84%", "Observation coverage", self.colors["warning"])

        self.draw_mini_bars(card2, [12, 18, 14, 22, 16, 26, 20], self.colors["accent"])
        self.draw_mini_bars(card3, [20, 24, 28, 22, 18, 25, 30], self.colors["warning"])
    
  
    def draw_soft_card(self, rect, title, value, subtitle="", accent_color=None):
        if accent_color is None:
            accent_color = self.colors["accent"]

        radius = 18


        shadow_rect = rect.move(0, 2)
        pygame.draw.rect(
            self.screen,
            (11, 8, 7),
            shadow_rect,
            border_radius=radius
        )

    
        pygame.draw.rect(
            self.screen,
            (48, 39, 36),
            rect,
            border_radius=radius
        )


        title_surf = self.fonts["small"].render(title, True, (156, 144, 139))
        self.screen.blit(title_surf, (rect.x + 20, rect.y + 8))

        value_surf = self.fonts["large"].render(value, True, (232, 236, 242))
        self.screen.blit(value_surf, (rect.x + 20, rect.y + 33))

        if subtitle:
            subtitle_surf = self.fonts["small"].render(subtitle, True, (176, 166, 160))
            self.screen.blit(subtitle_surf, (rect.x + 20, rect.bottom - 30))

        pill_rect = pygame.Rect(rect.right - 42, rect.y + 14, 24, 12)
        pygame.draw.rect(self.screen, (36, 46, 72), pill_rect, border_radius=6)
        pygame.draw.circle(
            self.screen,
            accent_color,
            (pill_rect.x + 8, pill_rect.y + pill_rect.height // 2),
            3
        )

    def draw_checklist_card(self, rect, title, pose, progress_data=None, accent_color=None):
        if accent_color is None:
            accent_color = self.colors["accent"]

        radius = 18

        shadow_rect = rect.move(0, 2)
        pygame.draw.rect(
            self.screen,
            (11, 8, 7),
            shadow_rect,
            border_radius=radius
        )

        pygame.draw.rect(
            self.screen,
            (48, 39, 36),
            rect,
            border_radius=radius
        )
        
        title_color = (156, 144, 139)
        section_color = (176, 166, 160)
        value_color = (232, 236, 242)

        title_surf = self.fonts["small"].render(title, True, title_color)
        self.screen.blit(title_surf, (rect.x + 20, rect.y + 8))

        
        live_pose_surf = self.fonts["medium"].render(pose, True, value_color)
        self.screen.blit(live_pose_surf, (rect.x + 20, rect.y + 33))

        sub_surf = self.fonts["small"].render("Required checks", True, section_color)
        self.screen.blit(sub_surf, (rect.x + 20, rect.y + 78))


        pygame.draw.line(
            self.screen,
            (70, 58, 54),
            (rect.x + 20, rect.y + 100),
            (rect.right - 20, rect.y + 100),
            1
        )

        
        if not progress_data:
            empty_surf = self.fonts["small"].render("No scene data", True, (130, 145, 170))
            self.screen.blit(empty_surf, (rect.x + 20, rect.y + 118))
            return

        expected = progress_data["expected"]
        step_results = progress_data["step_results"]
        current_index = progress_data["current_index"]

        start_y = rect.y + 116
        row_gap = 28

        for i, item in enumerate(expected):
            row_y = start_y + i * row_gap

            status = step_results[i]
            is_current = (current_index == i) if current_index is not None else False 

            if status == "correct":
                text_color = (220, 228, 236)
            elif status == "missed": 
                text_color = (170, 120, 120)
            elif is_current :
                text_color = (235, 238, 244)
            else :
                text_color = (130, 145, 170)

            center = (rect.x + 30, row_y + 8)

            pygame.draw.circle(self.screen, (36, 46, 72), center, 8)

            if status == "correct":
                pygame.draw.circle(self.screen, self.colors["success"], center, 4)
            elif status == "missed":
                pygame.draw.circle(self.screen, (170, 90, 90), center, 4)
            elif is_current:
                pygame.draw.circle(self.screen,accent_color, center, 7, 2)
            else : 
                pygame.draw.circle(self.screen, (90, 92, 100), center, 4, 1)

            label = self.better_pose_naming(item)
            item_surf = self.fonts["small"].render(label, True, text_color)
            self.screen.blit(item_surf, (rect.x + 48, row_y))
    
    def better_pose_naming(self, text) :

        mapping = {
            "TOP MIRROR": "Top Mirror",
            "LEFT MIRROR": "Left Mirror",
            "RIGHT MIRROR": "Right Mirror",
            "LEFT BLINDSPOT": "Left Blind Spot",
            "RIGHT BLINDSPOT": "Right Blind Spot",
            "LOOKING DOWN": "Looking Down",
            "FORWARD": "Forward"
        }   

        return mapping.get(text, text.title())



  