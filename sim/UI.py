import pygame 
import os 

class UI :
  
    def __init__(self, screen, screen_width, screen_height, ):
    
    
        base_dir = os.path.dirname(__file__)
        
        small_font_path = os.path.join(base_dir, "fonts", "Nunito-Regular.ttf")
        
        large_font_path = os.path.join(base_dir, "fonts", "Nunito-SemiBold.ttf")

        hero_title_font_path = os.path.join(base_dir, "fonts", "PlusJakartaSans-SemiBold.ttf")

        preview_path = os.path.join(base_dir, "Proto_images", "image.png")
        self.home_preview = pygame.image.load(preview_path).convert()
        
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
        "hero_small": pygame.font.Font(small_font_path, 14), 
        "hero": pygame.font.Font(hero_title_font_path, 85),
        "large": pygame.font.Font(large_font_path, 54)
    
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

        self.start_hover_t = 0.0
        self.scenario_hover_t = 0.0

        self.start_button_rect = None
        self.scenario_button_rect = None

        self.about_rect = None
        self.features_rect = None
        self.scenarios_rect = None
        self.login_rect = None
        self.signup_rect = None

        self.about_hover_t = 0.0
        self.features_hover_t = 0.0
        self.scenarios_hover_t = 0.0
        self.login_hover_t = 0.0
        self.signup_hover_t = 0.0

        
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


    def draw_homepage(self) :
       self.draw_home_background()
       shell_rect = self.draw_home_shell()
       self.draw_home_nav(shell_rect)
       self.draw_home_hero(shell_rect)
       self.draw_home_preview(shell_rect)
       self.draw_home_feature_pills(shell_rect)

    
    def draw_home_shell(self):
        margin_x = 20
        margin_y = 16
        radius = 32

        shell_rect = pygame.Rect(
            margin_x,
            margin_y,
            self.W - 2 * margin_x,
            self.H - 2 * margin_y
        )

        shadow_rect = shell_rect.move(0, 8)
        pygame.draw.rect(self.screen, (8, 7, 7), shadow_rect, border_radius=radius)
        pygame.draw.rect(self.screen, (30, 24, 22), shell_rect, border_radius=radius)

        return shell_rect
    
    def draw_home_background(self):
        top = (34, 28, 25)
        bottom = (14, 11, 10)

        for y in range(self.H):
            t = y / (self.H - 1)

            r = int(top[0] + (bottom[0] - top[0]) * t)
            g = int(top[1] + (bottom[1] - top[1]) * t)
            b = int(top[2] + (bottom[2] - top[2]) * t)

            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.W, y))

        glow = pygame.Surface((420, 420), pygame.SRCALPHA)
        pygame.draw.circle(glow, (110, 80, 60, 24), (210, 210), 210)
        self.screen.blit(glow, (self.W - 520, 120))

    
    def draw_home_preview(self, shell_rect):
        preview_w = 780
        preview_h = 420
        preview_x = shell_rect.right - preview_w - 70
        preview_y = shell_rect.y + 250
        radius = 26

        preview_rect = pygame.Rect(preview_x, preview_y, preview_w, preview_h)

        #pygame.draw.rect(
            #self.screen,
            #(26, 21, 20),
            #preview_rect,
            #border_radius=radius
        #)

       

        inset = 10
        image_rect = pygame.Rect(
            preview_rect.x + inset,
            preview_rect.y + inset,
            preview_rect.w - 2 * inset,
            preview_rect.h - 2 * inset
        )

        scaled_img = pygame.transform.smoothscale(self.home_preview, (image_rect.w, image_rect.h))

        image_surface = pygame.Surface((image_rect.w, image_rect.h), pygame.SRCALPHA)
        image_surface.blit(scaled_img, (0, 0))

        mask = pygame.Surface((image_rect.w, image_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(
            mask,
            (255, 255, 255, 255),
            (0, 0, image_rect.w, image_rect.h),
            border_radius=20
        )

        image_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(image_surface, (image_rect.x, image_rect.y))
    

    def draw_feature_pill(self, rect, title, subtitle, accent_color):
        radius = 18

        pygame.draw.rect(
            self.screen,
            (34, 28, 26),
            rect,
            border_radius=radius
        )

        
        title_surf = self.fonts["small"].render(title, True, (230, 234, 240))
        self.screen.blit(title_surf, (rect.x + 18, rect.y + 14))

        subtitle_surf = self.fonts["small"].render(subtitle, True, (156, 144, 139))
        self.screen.blit(subtitle_surf, (rect.x + 18, rect.y + 40))

        pygame.draw.circle(
            self.screen,
            accent_color,
            (rect.right - 18, rect.y + 18),
            4
        )
    

    def draw_home_feature_pills(self, shell_rect):
        preview_w = 630
        preview_h = 350
        preview_x = shell_rect.right - preview_w - 80
        preview_y = shell_rect.y + 220

        pill1 = pygame.Rect(preview_x - 150, preview_y + 1, 250, 82)
        pill2 = pygame.Rect(preview_x + preview_w - 180, preview_y + preview_h + 25, 250, 82)

        self.draw_feature_pill(
            pill1,
            "Live Head Tracking",
            "Panoramic view control",
            (82, 145, 255)
        )

        self.draw_feature_pill(
            pill2,
            "Observation Checks",
            "Mirror and blind spot review",
            (230, 180, 80)
        )
    

    def lerp_color(self, c1, c2, t) :
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )


    def draw_home_hero(self, shell_rect):
        hero_x = shell_rect.x + 70
        hero_y = shell_rect.y + 200

        mouse_pos = pygame.mouse.get_pos()

        eyebrow_color = (166, 154, 148)
        heading_color = (232, 236, 242)
        desc_color = (156, 144, 139)

        primary_fill = (58, 92, 160)
        primary_hover = (74, 110, 184)
        primary_text = (240, 243, 248)

        secondary_fill = (30, 24, 22)
        secondary_hover_fill = (38, 31, 29)
        secondary_border = (92, 76, 70)
        secondary_hover_border = (120, 100, 94)
        secondary_text = (220, 224, 232)

        eyebrow_surf = self.fonts["small"].render("Driving Awareness Training", True, eyebrow_color)
        self.screen.blit(eyebrow_surf, (hero_x, hero_y))

   
        heading1 = self.fonts["hero"].render("Driver Observation", True, heading_color)
        heading2 = self.fonts["hero"].render("Simulator", True, heading_color)

        heading_y = hero_y + 34
        self.screen.blit(heading1, (hero_x, heading_y))
        self.screen.blit(heading2, (hero_x, heading_y + heading1.get_height() - 12))

    
        desc_y = heading_y + heading1.get_height() + heading2.get_height() - 2

        desc1 = self.fonts["small"].render(
            "Track head movement across panoramic driving scenes",
            True,
            desc_color
        )
        desc2 = self.fonts["small"].render(
            "and evaluate mirror checks, blind spot checks,",
            True,
            desc_color
        )
        desc3 = self.fonts["small"].render(
            "and scan behavior in real time.",
            True,
            desc_color
        )

        self.screen.blit(desc1, (hero_x, desc_y + 18))
        self.screen.blit(desc2, (hero_x, desc_y + 44))
        self.screen.blit(desc3, (hero_x, desc_y + 70))

        button_y = desc_y + 135
        start_base = pygame.Rect(hero_x, button_y, 180, 50)
        scenario_base = pygame.Rect(hero_x + 200, button_y, 180, 50)

        
        start_hovered = start_base.collidepoint(mouse_pos)
        scenario_hovered = scenario_base.collidepoint(mouse_pos)

        
        speed = 0.30
        self.start_hover_t += ((1.0 if start_hovered else 0.0) - self.start_hover_t) * speed
        self.scenario_hover_t += ((1.0 if scenario_hovered else 0.0) - self.scenario_hover_t) * speed

        start_lift = int(round(2 * self.start_hover_t))
        scenario_lift = int(round(2 * self.scenario_hover_t))

        start_rect = start_base.move(0, -start_lift)
        scenario_rect = scenario_base.move(0, -scenario_lift)


        self.start_button_rect = start_rect
        self.scenario_button_rect = scenario_rect

        start_fill_color = self.lerp_color(primary_fill, primary_hover, self.start_hover_t)
        scenario_fill_color = self.lerp_color(secondary_fill, secondary_hover_fill, self.scenario_hover_t)
        scenario_border_color = self.lerp_color(secondary_border, secondary_hover_border, self.scenario_hover_t)

    
        #start_shadow = start_rect.move(0, 4)
        #pygame.draw.rect(self.screen, (24, 20, 19), start_shadow, border_radius=14)
        pygame.draw.rect(self.screen, start_fill_color, start_rect, border_radius=18)

        start_surf = self.fonts["small"].render("Start Session", True, primary_text)
        start_text_rect = start_surf.get_rect(center=start_rect.center)
        self.screen.blit(start_surf, start_text_rect)

        scenario_shadow = scenario_rect.move(0, 4)
        pygame.draw.rect(self.screen, (24, 20, 19), scenario_shadow, border_radius=18)
        pygame.draw.rect(self.screen, scenario_fill_color, scenario_rect, border_radius=18)
        pygame.draw.rect(self.screen, scenario_border_color, scenario_rect, width=1, border_radius=18)

        scenario_surf = self.fonts["small"].render("Select Scenario", True, secondary_text)
        scenario_text_rect = scenario_surf.get_rect(center=scenario_rect.center)
        self.screen.blit(scenario_surf, scenario_text_rect)
    
    def draw_home_nav(self, shell_rect):
        nav_y = shell_rect.y + 28
        pad_x = 40
        mouse_pos = pygame.mouse.get_pos()
        speed = 0.30

        brand_color = (232, 236, 242)

        nav_base = (150, 142, 138)
        nav_hover = (214, 218, 224)

        login_base = (180, 172, 168)
        login_hover = (228, 232, 238)

        signup_fill = (30, 24, 22)
        signup_hover_fill = (38, 31, 29)
        signup_border = (92, 76, 70)
        signup_hover_border = (125, 104, 98)
        signup_text_base = (232, 236, 242)
        signup_text_hover = (245, 247, 250)

        brand_surf = self.fonts["medium"].render("LookFirst", True, brand_color)
        self.screen.blit(brand_surf, (shell_rect.x + pad_x, nav_y))

        links = ["About", "Features", "Scenarios"]
        link_spacing = 110
        center_start_x = shell_rect.centerx - 140

        link_data = [
            ("about", links[0], center_start_x),
            ("features", links[1], center_start_x + link_spacing),
            ("scenarios", links[2], center_start_x + 2 * link_spacing),
        ]

        for key, label, x in link_data:
            base_surf = self.fonts["small"].render(label, True, nav_base)
            rect = base_surf.get_rect(topleft=(x, nav_y + 4))
            hovered = rect.collidepoint(mouse_pos)

            if key == "about":
                self.about_hover_t += ((1.0 if hovered else 0.0) - self.about_hover_t) * speed
                hover_t = self.about_hover_t
                self.about_rect = rect
            elif key == "features":
                self.features_hover_t += ((1.0 if hovered else 0.0) - self.features_hover_t) * speed
                hover_t = self.features_hover_t
                self.features_rect = rect
            else:
                self.scenarios_hover_t += ((1.0 if hovered else 0.0) - self.scenarios_hover_t) * speed
                hover_t = self.scenarios_hover_t
                self.scenarios_rect = rect

            text_color = self.lerp_color(nav_base, nav_hover, hover_t)
            link_surf = self.fonts["small"].render(label, True, text_color)
            self.screen.blit(link_surf, rect.topleft)

            underline_w = int(rect.w * hover_t)
            if underline_w > 0:
                underline_rect = pygame.Rect(rect.x, rect.bottom + 4, underline_w, 2)
                pygame.draw.rect(self.screen, (110, 140, 210), underline_rect, border_radius=1)

        signup_base = pygame.Rect(shell_rect.right - pad_x - 120, nav_y - 6, 120, 40)
        signup_hovered = signup_base.collidepoint(mouse_pos)
        self.signup_hover_t += ((1.0 if signup_hovered else 0.0) - self.signup_hover_t) * speed

        signup_lift = int(round(1 * self.signup_hover_t))
        signup_rect = signup_base.move(0, -signup_lift)
        self.signup_rect = signup_rect

        signup_fill_color = self.lerp_color(signup_fill, signup_hover_fill, self.signup_hover_t)
        signup_border_color = self.lerp_color(signup_border, signup_hover_border, self.signup_hover_t)
        signup_text_color = self.lerp_color(signup_text_base, signup_text_hover, self.signup_hover_t)

        pygame.draw.rect(self.screen, signup_fill_color, signup_rect, border_radius=12)
        pygame.draw.rect(self.screen, signup_border_color, signup_rect, width=1, border_radius=12)

        signup_surf = self.fonts["small"].render("Sign Up", True, signup_text_color)
        signup_text_rect = signup_surf.get_rect(center=signup_rect.center)
        self.screen.blit(signup_surf, signup_text_rect)

        login_surf_base = self.fonts["small"].render("Log In", True, login_base)
        login_rect = login_surf_base.get_rect(topleft=(signup_rect.x - 62, nav_y + 4))
        login_hovered = login_rect.collidepoint(mouse_pos)

        self.login_hover_t += ((1.0 if login_hovered else 0.0) - self.login_hover_t) * speed
        self.login_rect = login_rect

        login_color = self.lerp_color(login_base, login_hover, self.login_hover_t)
        login_surf = self.fonts["small"].render("Log In", True, login_color)
        self.screen.blit(login_surf, login_rect.topleft)
    

    def get_home_click_target(self, mouse_pos) :

        if self.start_button_rect and self.start_button_rect.collidepoint(mouse_pos) :
            return "start_session"

        if self.scenario_button_rect and self.scenario_button_rect.collidepoint(mouse_pos):
            return "select_scenario"

        if self.about_rect and self.about_rect.collidepoint(mouse_pos):
            return "about"

        if self.features_rect and self.features_rect.collidepoint(mouse_pos):
            return "features"

        if self.scenarios_rect and self.scenarios_rect.collidepoint(mouse_pos):
            return "scenarios"

        if self.login_rect and self.login_rect.collidepoint(mouse_pos):
            return "login"

        if self.signup_rect and self.signup_rect.collidepoint(mouse_pos):
            return "signup"

        return None
    

    def draw_scene_select(self) :
        self.draw_home_background()
        shell_rect = self.draw_home_shell()
        self.draw_scene_select_header(shell_rect)
        self.draw_scene_cards(shell_rect)
        self.draw_home_nav(shell_rect)


    def draw_scene_card(self, rect, title, subtitle, tag, accent_color):
        radius = 22

        shadow_rect = rect.move(0, 5)
        pygame.draw.rect(self.screen, (24, 20, 19), shadow_rect, border_radius=radius)

        pygame.draw.rect(self.screen, (34, 28, 26), rect, border_radius=radius)
        pygame.draw.rect(self.screen, (70, 58, 54), rect, width=1, border_radius=radius)

        tag_rect = pygame.Rect(rect.x + 20, rect.y + 18, 90, 28)
        pygame.draw.rect(self.screen, (42, 34, 31), tag_rect, border_radius=10)
        pygame.draw.circle(self.screen, accent_color, (tag_rect.x + 14, tag_rect.centery), 4)

        tag_surf = self.fonts["hero_small"].render(tag, True, (210, 216, 224))
        self.screen.blit(tag_surf, (tag_rect.x + 24, tag_rect.y + 5))

        title_surf = self.fonts["medium"].render(title, True, (232, 236, 242))
        self.screen.blit(title_surf, (rect.x + 20, rect.y + 72))

 
        sub1 = self.fonts["small"].render(subtitle[0], True, (156, 144, 139))
        sub2 = self.fonts["small"].render(subtitle[1], True, (156, 144, 139))
        self.screen.blit(sub1, (rect.x + 20, rect.y + 110))
        self.screen.blit(sub2, (rect.x + 20, rect.y + 136))

  
        button_rect = pygame.Rect(rect.x + 20, rect.bottom - 60, rect.w - 40, 42)
        pygame.draw.rect(self.screen, (42, 34, 31), button_rect, border_radius=12)
        pygame.draw.rect(self.screen, (82, 70, 66), button_rect, width=1, border_radius=12)

        button_surf = self.fonts["small"].render("Select Scenario", True, (230, 234, 240))
        button_text_rect = button_surf.get_rect(center=button_rect.center)
        self.screen.blit(button_surf, button_text_rect)
    

    def draw_scene_cards(self, shell_rect):
        card_w = 500
        card_h = 460
        gap = 40

        total_w = 3 * card_w + 2 * gap
        start_x = shell_rect.centerx - total_w // 2
        y = shell_rect.y + 300

        card1 = pygame.Rect(start_x, y, card_w, card_h)
        card2 = pygame.Rect(start_x + card_w + gap, y, card_w, card_h)
        card3 = pygame.Rect(start_x + 2 * (card_w + gap), y, card_w, card_h)

        self.draw_scene_card(
            card1,
            "Left Lane Change",
            ("Checks mirror and blind spot", "sequence before lane movement."),
            "Sequence",
            (82, 145, 255)
        )

        self.draw_scene_card(
            card2,
            "Four-Way Left Turn",
            ("Evaluates observation coverage", "through an intersection turn."),
            "Coverage",
            (230, 180, 80)
        )

        self.draw_scene_card(
            card3,
            "More Coming Soon",
            ("Additional driving scenarios", "are currently in development."),
            "Soon",
            (120, 170, 140)
        )

    def draw_scene_select_header(self, shell_rect):
        x = shell_rect.x + 70
        y = shell_rect.y + 90

        title_surf = self.fonts["hero"].render("Select a Scenario", True, (232, 236, 242))
        self.screen.blit(title_surf, (x, y))

        sub_surf = self.fonts["small"].render(
            "Choose a driving situation to begin a guided observation session.",
            True,
            (156, 144, 139)
        )
        self.screen.blit(sub_surf, (x, y + 115))