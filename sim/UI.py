import pygame 
import os 

class UI :
  
    def __init__(self, screen, screen_width, screen_height, ):
    
    
        base_dir = os.path.dirname(__file__)
        
        small_font_path = os.path.join(base_dir, "fonts", "Nunito-Regular.ttf")
        
        large_font_path = os.path.join(base_dir, "fonts", "Nunito-SemiBold.ttf")

        hero_title_font_path = os.path.join(base_dir, "fonts", "PlusJakartaSans-SemiBold.ttf")

        preview_path = os.path.join(base_dir, "Proto_images", "image.png")
        select_scene_1 = os.path.join(base_dir, "Proto_images", "select_scene_01.png")
        select_scene_2 = os.path.join(base_dir, "Proto_images", "select_scene_02.png")
        self.home_preview = pygame.image.load(preview_path).convert()
        self.select_scene_1 = pygame.image.load(select_scene_1).convert()
        self.select_scene_2 = pygame.image.load(select_scene_2).convert()
        
        self.W = screen_width
        self.H = screen_height
        self.screen = screen 
        self.panel_size = 150
        
        self.colors = {
           "background": (232, 224, 214),
    "top_grad": (238, 230, 220),
    "bottom_grad": (220, 210, 198),
    "glow": (204, 186, 166),

    "shell": (244, 238, 230),
    "shell_shadow": (198, 184, 170),

    "surface": (255, 252, 247),
    "surface_2": (246, 240, 232),
    "surface_3": (238, 230, 220),
    "surface_hover": (230, 222, 212),
    "surface_shadow": (208, 196, 182),

    "border": (206, 192, 176),
    "border_strong": (184, 170, 154),
    "border_hover": (158, 142, 124),
    "divider": (214, 200, 184),

    "text": (48, 36, 26),
    "text_soft": (72, 56, 42),
    "text_muted": (104, 88, 72),
    "text_subtle": (124, 106, 88),
    "text_faint": (148, 128, 110),
    "text_disabled": (166, 146, 128),

    "accent": (172, 118, 70),
    "accent_hover": (190, 132, 82),
    "accent_alt": (204, 150, 100),

    "success": (104, 156, 120),
    "warning": (208, 156, 86),
    "danger": (188, 96, 88),
    "danger_text": (160, 112, 106),

    "chip": (240, 232, 222),
    "chip_text": (86, 66, 46),

    "overlay_tint": (228, 220, 210),
    "fade": (222, 214, 204),

    "viewport_outer": (222, 212, 200),
    "viewport_inner": (210, 198, 186),
    "indicator_bg": (224, 212, 198),
    "indicator_idle": (150, 136, 120),

    "panel": (228, 218, 206),
    "card_shadow": (188, 174, 158),
    "card_outer": (222, 212, 200),
    "card_inner": (210, 198, 186),
    "card_border": (182, 166, 148),

    "muted": (132, 114, 96),

    "scene_card_1": (210, 150, 90),
    "scene_card_2": (162, 120, 84),
    "scene_card_3": (224, 176, 112)
}
        
        self.fonts = {
        "small": pygame.font.Font(small_font_path, 16),
        "medium": pygame.font.Font(small_font_path, 22), 
        "hero_small": pygame.font.Font(small_font_path, 14),
        "intro_small": pygame.font.Font(small_font_path, 19), 
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

        self.scene_card_1_rect = None
        self.scene_card_2_rect = None
        self.scene_card_3_rect = None

        self.scene_card_1_hover_t = 0.0
        self.scene_card_2_hover_t = 0.0
        self.scene_card_3_hover_t = 0.0

        self.start_intro_button_rect = None
        self.back_intro_button_rect = None

        self.start_intro_hover_t = 0.0
        self.back_intro_hover_t = 0.0

        self.retry_button_rect = None
        self.results_back_button_rect = None

        self.retry_hover_t = 0.0
        self.results_back_hover_t = 0.0

        
    def draw_background_components(self) :
    
      self.draw_background()
      self.draw_vertical_gradient()
      self.draw_view_shell()
    
    def c(self, key) :
        return self.colors[key]
  
    def draw_background(self):
        self.screen.fill(self.c("background"))
    
    def draw_overlay(self, pose, progress_data=None) :
        self.draw_smaller_cards(pose, progress_data)


    def draw_vertical_gradient(self):
        top = self.c("top_grad")
        bottom = self.c("bottom_grad")

        for y in range(self.H):
            t = y / (self.H - 1)

            r = int(top[0] + (bottom[0] - top[0]) * t)
            g = int(top[1] + (bottom[1] - top[1]) * t)
            b = int(top[2] + (bottom[2] - top[2]) * t)

            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.W - 1, y))


    def draw_view_shell(self):
        rect = self.viewport_rect

        pygame.draw.rect(
            self.screen,
            self.c("viewport_outer"),
            rect.inflate(14, 14),
            border_radius=12
        )

        pygame.draw.rect(
            self.screen,
            self.c("viewport_inner"),
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
            accent_color = self.c("accent")

        radius = 18

        shadow_rect = rect.move(0, 2)
        pygame.draw.rect(
            self.screen,
            self.c("surface_shadow"),
            shadow_rect,
            border_radius=radius
        )

        pygame.draw.rect(
            self.screen,
            self.c("surface_3"),
            rect,
            border_radius=radius
        )

        title_surf = self.fonts["small"].render(title, True, self.c("text_faint"))
        self.screen.blit(title_surf, (rect.x + 20, rect.y + 8))

        value_surf = self.fonts["large"].render(value, True, self.c("text"))
        self.screen.blit(value_surf, (rect.x + 20, rect.y + 33))

        if subtitle:
            subtitle_surf = self.fonts["small"].render(subtitle, True, self.c("text_muted"))
            self.screen.blit(subtitle_surf, (rect.x + 20, rect.bottom - 30))

        pill_rect = pygame.Rect(rect.right - 42, rect.y + 14, 24, 12)
        pygame.draw.rect(self.screen, self.c("indicator_bg"), pill_rect, border_radius=6)
        pygame.draw.circle(
            self.screen,
            accent_color,
            (pill_rect.x + 8, pill_rect.y + pill_rect.height // 2),
            3
        )


    def draw_checklist_card(self, rect, title, pose, progress_data=None, accent_color=None):
        if accent_color is None:
            accent_color = self.c("accent")

        radius = 18

        shadow_rect = rect.move(0, 2)
        pygame.draw.rect(
            self.screen,
            self.c("surface_shadow"),
            shadow_rect,
            border_radius=radius
        )

        pygame.draw.rect(
            self.screen,
            self.c("surface_3"),
            rect,
            border_radius=radius
        )

        title_color = self.c("text_faint")
        section_color = self.c("text_muted")
        value_color = self.c("text")

        title_surf = self.fonts["small"].render(title, True, title_color)
        self.screen.blit(title_surf, (rect.x + 20, rect.y + 8))

        live_pose_surf = self.fonts["medium"].render(pose, True, value_color)
        self.screen.blit(live_pose_surf, (rect.x + 20, rect.y + 33))

        sub_surf = self.fonts["small"].render("Required checks", True, section_color)
        self.screen.blit(sub_surf, (rect.x + 20, rect.y + 78))

        pygame.draw.line(
            self.screen,
            self.c("divider"),
            (rect.x + 20, rect.y + 100),
            (rect.right - 20, rect.y + 100),
            1
        )

        if not progress_data:
            empty_surf = self.fonts["small"].render("No scene data", True, self.c("text_disabled"))
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
                text_color = self.c("text_soft")
            elif status == "missed":
                text_color = self.c("danger_text")
            elif is_current:
                text_color = self.c("text")
            else:
                text_color = self.c("text_disabled")

            center = (rect.x + 30, row_y + 8)

            pygame.draw.circle(self.screen, self.c("indicator_bg"), center, 8)

            if status == "correct":
                pygame.draw.circle(self.screen, self.c("success"), center, 4)
            elif status == "missed":
                pygame.draw.circle(self.screen, self.c("danger"), center, 4)
            elif is_current:
                pygame.draw.circle(self.screen, accent_color, center, 7, 2)
            else:
                pygame.draw.circle(self.screen, self.c("indicator_idle"), center, 4, 1)

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

        
    def draw_home_background(self):
        top = self.c("top_grad")
        bottom = self.c("bottom_grad")

        for y in range(self.H):
            t = y / (self.H - 1)

            r = int(top[0] + (bottom[0] - top[0]) * t)
            g = int(top[1] + (bottom[1] - top[1]) * t)
            b = int(top[2] + (bottom[2] - top[2]) * t)

            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.W, y))

        glow = pygame.Surface((420, 420), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*self.c("glow"), 24), (210, 210), 210)
        self.screen.blit(glow, (self.W - 520, 120))


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
        pygame.draw.rect(self.screen, self.c("shell_shadow"), shadow_rect, border_radius=radius)
        pygame.draw.rect(self.screen, self.c("shell"), shell_rect, border_radius=radius)

        return shell_rect


    def draw_home_preview(self, shell_rect):
        preview_w = 780
        preview_h = 420
        preview_x = shell_rect.right - preview_w - 70
        preview_y = shell_rect.y + 250
        radius = 26

        preview_rect = pygame.Rect(preview_x, preview_y, preview_w, preview_h)

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
            self.c("surface"),
            rect,
            border_radius=radius
        )

        title_surf = self.fonts["small"].render(title, True, self.c("text_soft"))
        self.screen.blit(title_surf, (rect.x + 18, rect.y + 14))

        subtitle_surf = self.fonts["small"].render(subtitle, True, self.c("text_faint"))
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

        eyebrow_color = self.c("text_subtle")
        heading_color = self.c("text")
        desc_color = self.c("text_faint")

        primary_fill = self.c("accent")
        primary_hover = self.c("accent_hover")
        primary_text = self.c("text")

        secondary_fill = self.c("shell")
        secondary_hover_fill = self.c("surface_hover")
        secondary_border = self.c("border_strong")
        secondary_hover_border = self.c("border_hover")
        secondary_text = self.c("text_soft")

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

        pygame.draw.rect(self.screen, start_fill_color, start_rect, border_radius=18)

        start_surf = self.fonts["small"].render("Start Session", True, primary_text)
        start_text_rect = start_surf.get_rect(center=start_rect.center)
        self.screen.blit(start_surf, start_text_rect)

        scenario_shadow = scenario_rect.move(0, 4)
        pygame.draw.rect(self.screen, self.c("surface_shadow"), scenario_shadow, border_radius=36)
        pygame.draw.rect(self.screen, scenario_fill_color, scenario_rect, border_radius=18)
        pygame.draw.rect(self.screen, scenario_border_color, scenario_rect, width=1, border_radius=36)

        scenario_surf = self.fonts["small"].render("Select Scenario", True, secondary_text)
        scenario_text_rect = scenario_surf.get_rect(center=scenario_rect.center)
        self.screen.blit(scenario_surf, scenario_text_rect)
        
    def draw_home_nav(self, shell_rect):
        nav_y = shell_rect.y + 28
        pad_x = 40
        mouse_pos = pygame.mouse.get_pos()
        speed = 0.30

        brand_color = self.c("text")
        nav_base = self.c("text_faint")
        nav_hover = self.c("text_soft")

        login_base = self.c("text_muted")
        login_hover = self.c("text_soft")

        signup_fill = self.c("shell")
        signup_hover_fill = self.c("surface_hover")
        signup_border = self.c("border_strong")
        signup_hover_border = self.c("border_hover")
        signup_text_base = self.c("text")
        signup_text_hover = self.c("text")

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
                pygame.draw.rect(self.screen, self.c("accent_alt"), underline_rect, border_radius=1)

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


    def draw_scene_select_header(self, shell_rect):
        x = shell_rect.x + 70
        y = shell_rect.y + 90

        title_surf = self.fonts["hero"].render("Select a Scenario", True, self.c("text"))
        self.screen.blit(title_surf, (x, y))

        sub_surf = self.fonts["small"].render(
            "Choose a driving situation to begin a guided observation session.",
            True,
            self.c("text_faint")
        )
        self.screen.blit(sub_surf, (x, y + 115))
    
    def draw_scene_card(self, rect, title, subtitle, tag, accent_color, image, hover_t):
        radius = 22

        border_base = self.c("border")
        border_hover = self.c("border_hover")
        border_color = self.lerp_color(border_base, border_hover, hover_t)

        shadow_rect = rect.move(0, 5)
        pygame.draw.rect(self.screen, self.c("surface_shadow"), shadow_rect, border_radius=radius)

        pygame.draw.rect(self.screen, self.c("surface"), rect, border_radius=radius)
        pygame.draw.rect(self.screen, border_color, rect, width=1, border_radius=radius)

        image_extra_h = int(round(20 * hover_t))
        image_rect = pygame.Rect(
            rect.x + 16,
            rect.y + 16,
            rect.w - 32,
            165 + image_extra_h
        )

        pygame.draw.rect(self.screen, self.c("shell"), image_rect, border_radius=16)

        scaled_img = pygame.transform.smoothscale(image, (image_rect.w, image_rect.h))
        image_surface = pygame.Surface((image_rect.w, image_rect.h), pygame.SRCALPHA)
        image_surface.blit(scaled_img, (0, 0))

        mask = pygame.Surface((image_rect.w, image_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, image_rect.w, image_rect.h), border_radius=16)
        image_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.screen.blit(image_surface, (image_rect.x, image_rect.y))

        content_shift = image_extra_h

        tag_rect = pygame.Rect(rect.x + 20, rect.y + 195 + content_shift, 90, 28)
        pygame.draw.rect(self.screen, self.c("chip"), tag_rect, border_radius=10)
        pygame.draw.circle(self.screen, accent_color, (tag_rect.x + 14, tag_rect.centery), 4)

        tag_surf = self.fonts["hero_small"].render(tag, True, self.c("chip_text"))
        self.screen.blit(tag_surf, (tag_rect.x + 24, tag_rect.y + 5))

        title_surf = self.fonts["medium"].render(title, True, self.c("text"))
        self.screen.blit(title_surf, (rect.x + 20, rect.y + 238 + content_shift))

        sub1 = self.fonts["small"].render(subtitle[0], True, self.c("text_faint"))
        sub2 = self.fonts["small"].render(subtitle[1], True, self.c("text_faint"))
        self.screen.blit(sub1, (rect.x + 20, rect.y + 278 + content_shift))
        self.screen.blit(sub2, (rect.x + 20, rect.y + 304 + content_shift))

        button_rect = pygame.Rect(rect.x + 20, rect.bottom - 60, rect.w - 40, 42)
        pygame.draw.rect(self.screen, self.c("surface_2"), button_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.c("border_strong"), button_rect, width=1, border_radius=12)

        button_surf = self.fonts["small"].render("Select Scenario", True, self.c("text_soft"))
        button_text_rect = button_surf.get_rect(center=button_rect.center)
        self.screen.blit(button_surf, button_text_rect)
    
    def draw_scene_cards(self, shell_rect):
        mouse_pos = pygame.mouse.get_pos()
        speed = 0.43

        card_w = 540
        card_h = 480
        gap = 40

        total_w = 3 * card_w + 2 * gap
        start_x = shell_rect.centerx - total_w // 2
        y = shell_rect.y + 300

        base_card1 = pygame.Rect(start_x, y, card_w, card_h)
        base_card2 = pygame.Rect(start_x + card_w + gap, y, card_w, card_h)
        base_card3 = pygame.Rect(start_x + 2 * (card_w + gap), y, card_w, card_h)

        hovered1 = base_card1.collidepoint(mouse_pos)
        hovered2 = base_card2.collidepoint(mouse_pos)
        hovered3 = base_card3.collidepoint(mouse_pos)

        self.scene_card_1_hover_t += ((1.0 if hovered1 else 0.0) - self.scene_card_1_hover_t) * speed
        self.scene_card_2_hover_t += ((1.0 if hovered2 else 0.0) - self.scene_card_2_hover_t) * speed
        self.scene_card_3_hover_t += ((1.0 if hovered3 else 0.0) - self.scene_card_3_hover_t) * speed

        lift1 = int(round(4 * self.scene_card_1_hover_t))
        lift2 = int(round(4 * self.scene_card_2_hover_t))
        lift3 = int(round(4 * self.scene_card_3_hover_t))

        card1 = base_card1.move(0, -lift1)
        card2 = base_card2.move(0, -lift2)
        card3 = base_card3.move(0, -lift3)

        self.scene_card_1_rect = card1
        self.scene_card_2_rect = card2
        self.scene_card_3_rect = card3

        self.draw_scene_card(
            card1,
            "Left Lane Change",
            ("Checks mirror and blind spot", "sequence before lane movement."),
            "Sequence",
            self.c("scene_card_1"),
            self.select_scene_2,
            self.scene_card_1_hover_t
        )

        self.draw_scene_card(
            card2,
            "Four-Way Left Turn",
            ("Evaluates observation coverage", "through an intersection turn."),
            "Coverage",
            self.c("scene_card_2"),
            self.select_scene_1,
            self.scene_card_2_hover_t
        )

        self.draw_scene_card(
            card3,
            "More Coming Soon",
            ("Additional driving scenarios", "are currently in development."),
            "Soon",
            self.c("scene_card_3"),
            self.home_preview,
            self.scene_card_3_hover_t
        )
    
    
    def get_scene_select_click_target(self, mouse_pos):
        if self.scene_card_1_rect and self.scene_card_1_rect.collidepoint(mouse_pos):
            return "left_lane_change"

        if self.scene_card_2_rect and self.scene_card_2_rect.collidepoint(mouse_pos):
            return "four_way_left_turn"

        if self.scene_card_3_rect and self.scene_card_3_rect.collidepoint(mouse_pos):
            return "coming_soon"

        return None
    

    def draw_scene_intro(self, scene_data) :
        self.draw_home_background()
        shell_rect = self.draw_home_shell()
        self.draw_home_nav(shell_rect)

        if not scene_data :
            return 

        self.draw_scene_intro_preview(shell_rect, scene_data)
        self.draw_scene_intro_details(shell_rect, scene_data)
    

    def draw_scene_intro_preview(self, shell_rect, scene_data):
        image_key = scene_data["image_key"]
        image = getattr(self, image_key)

        preview_rect = pygame.Rect(
            shell_rect.x + 34,
            shell_rect.y + 86,
            shell_rect.w - 68,
            420
        )

        shadow_rect = preview_rect.move(0, 6)
        pygame.draw.rect(self.screen, self.c("surface_shadow"), shadow_rect, border_radius=26)

        pygame.draw.rect(self.screen, self.c("shell"), preview_rect, border_radius=26)
        pygame.draw.rect(self.screen, self.c("border"), preview_rect, width=1, border_radius=26)

        scaled_img = pygame.transform.smoothscale(image, (preview_rect.w, preview_rect.h))
        image_surface = pygame.Surface((preview_rect.w, preview_rect.h), pygame.SRCALPHA)
        image_surface.blit(scaled_img, (0, 0))

        mask = pygame.Surface((preview_rect.w, preview_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(
            mask,
            (255, 255, 255, 255),
            (0, 0, preview_rect.w, preview_rect.h),
            border_radius=26
        )
        image_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.screen.blit(image_surface, (preview_rect.x, preview_rect.y))

        overlay = pygame.Surface((preview_rect.w, preview_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (*self.c("overlay_tint"), 24), (0, 0, preview_rect.w, preview_rect.h), border_radius=26)
        self.screen.blit(overlay, (preview_rect.x, preview_rect.y))

    def draw_scene_intro_details(self, shell_rect, scene_data):
        mouse_pos = pygame.mouse.get_pos()
        speed = 0.30

        content_x = shell_rect.x + 45
        content_y = shell_rect.y + 520

        title_color = self.c("text")
        desc_color = self.c("text_faint")
        section_color = self.c("text_muted")

        chip_fill = self.c("chip")
        chip_text = self.c("text_soft")

        primary_fill = self.c("accent")
        primary_hover = self.c("accent_hover")
        primary_text = self.c("text")

        secondary_fill = self.c("shell")
        secondary_hover_fill = self.c("surface_hover")
        secondary_border = self.c("border_strong")
        secondary_hover_border = self.c("border_hover")
        secondary_text = self.c("text_soft")

        chip_label = f'{scene_data["scenario_type"]} Scenario'
        chip_surf = self.fonts["small"].render(chip_label, True, chip_text)
        chip_rect = pygame.Rect(content_x, content_y + 20, chip_surf.get_width() + 28, 30)

        pygame.draw.rect(self.screen, chip_fill, chip_rect, border_radius=12)
        self.screen.blit(chip_surf, (chip_rect.x + 14, chip_rect.y + 5))

        title_surf = self.fonts["hero"].render(scene_data["title"], True, title_color)
        self.screen.blit(title_surf, (content_x, content_y + 75))

        desc = scene_data["description"]
        desc_surf = self.fonts["small"].render(desc, True, desc_color)
        self.screen.blit(desc_surf, (content_x, content_y + 190))

        section_surf = self.fonts["small"].render("Required Checks", True, section_color)
        self.screen.blit(section_surf, (content_x, content_y + 270))

        checks = scene_data["required_checks"]
        list_y = content_y + 300
        row_gap = 30

        for i, item in enumerate(checks):
            row_y = list_y + i * row_gap
            center = (content_x + 8, row_y + 9)

            pygame.draw.circle(self.screen, self.c("chip"), center, 8)
            pygame.draw.circle(self.screen, self.c("accent_alt"), center, 4)

            label = self.better_pose_naming(item)
            item_surf = self.fonts["small"].render(label, True, self.c("text_soft"))
            self.screen.blit(item_surf, (content_x + 24, row_y))

        button_y = content_y + 450
        button_x = shell_rect.right - 1850

        start_base = pygame.Rect(button_x, button_y, 180, 50)
        back_base = pygame.Rect(button_x + 200, button_y, 180, 50)

        start_hovered = start_base.collidepoint(mouse_pos)
        back_hovered = back_base.collidepoint(mouse_pos)

        self.start_intro_hover_t += ((1.0 if start_hovered else 0.0) - self.start_intro_hover_t) * speed
        self.back_intro_hover_t += ((1.0 if back_hovered else 0.0) - self.back_intro_hover_t) * speed

        start_lift = int(round(2 * self.start_intro_hover_t))
        back_lift = int(round(2 * self.back_intro_hover_t))

        start_rect = start_base.move(0, -start_lift)
        back_rect = back_base.move(0, -back_lift)

        self.start_intro_button_rect = start_rect
        self.back_intro_button_rect = back_rect

        start_fill = self.lerp_color(primary_fill, primary_hover, self.start_intro_hover_t)
        back_fill = self.lerp_color(secondary_fill, secondary_hover_fill, self.back_intro_hover_t)
        back_border = self.lerp_color(secondary_border, secondary_hover_border, self.back_intro_hover_t)

        pygame.draw.rect(self.screen, self.c("surface_shadow"), start_rect.move(0, 4), border_radius=14)
        pygame.draw.rect(self.screen, start_fill, start_rect, border_radius=14)

        start_surf = self.fonts["small"].render("Start Simulation", True, primary_text)
        start_text_rect = start_surf.get_rect(center=start_rect.center)
        self.screen.blit(start_surf, start_text_rect)

        pygame.draw.rect(self.screen, self.c("surface_shadow"), back_rect.move(0, 4), border_radius=14)
        pygame.draw.rect(self.screen, back_fill, back_rect, border_radius=14)
        pygame.draw.rect(self.screen, back_border, back_rect, width=1, border_radius=14)

        back_surf = self.fonts["small"].render("Back to Scenarios", True, secondary_text)
        back_text_rect = back_surf.get_rect(center=back_rect.center)
        self.screen.blit(back_surf, back_text_rect)
        
    def get_scene_intro_click_target(self, mouse_pos):
        if self.start_intro_button_rect and self.start_intro_button_rect.collidepoint(mouse_pos):
            return "start_simulation"

        if self.back_intro_button_rect and self.back_intro_button_rect.collidepoint(mouse_pos):
            return "back_to_scenarios"

        return None


    def draw_results(self, scene_data, score, result) :

        self.draw_home_background()
        shell_rect = self.draw_home_shell()
        self.draw_home_nav(shell_rect)

        scene_title = "Session Results"
        if scene_data :
            scene_title = scene_data["title"]

        self.draw_results_header(shell_rect, scene_title)
        self.draw_results_content(shell_rect, scene_data, score, result)
    

    def draw_results_header(self, shell_rect, scene_title):
        x = shell_rect.x + 70
        y = shell_rect.y + 95

        title_surf = self.fonts["hero"].render("Session Complete", True, self.c("text"))
        self.screen.blit(title_surf, (x, y))

        sub_surf = self.fonts["medium"].render(scene_title, True, self.c("text_muted"))
        self.screen.blit(sub_surf, (x, y + 113))

    def draw_results_content(self, shell_rect, scene_data, score, result):
        if score is None:
            score = 0

        expected = []
        statuses = []

        if scene_data:
            expected = scene_data["required_checks"]

        if isinstance(result, list):
            statuses = result

        if not expected and statuses:
            expected = [f"STEP {i+1}" for i in range(len(statuses))]

        completed = []
        missed = []

        for i, status in enumerate(statuses):
            label = expected[i] if i < len(expected) else f"Step {i+1}"

            if status == "correct":
                completed.append(label)
            elif status == "missed":
                missed.append(label)

        score_x = shell_rect.x + 70
        score_y = shell_rect.y + 245

        score_label_surf = self.fonts["small"].render("Overall Score", True, self.c("text_subtle"))
        self.screen.blit(score_label_surf, (score_x, score_y))

        score_text = f"{int(round(score))}%"
        score_surf = self.fonts["hero"].render(score_text, True, self.c("text"))
        self.screen.blit(score_surf, (score_x, score_y + 28))

        detail_y = shell_rect.y + 500
        card_w = 600
        card_h = 330
        gap = 28

        completed_rect = pygame.Rect(shell_rect.x + 70, detail_y, card_w, card_h)
        missed_rect = pygame.Rect(shell_rect.x + 70 + card_w + gap, detail_y, card_w, card_h)

        self.draw_results_list_card(completed_rect, "Completed", completed, self.c("success"))
        self.draw_results_list_card(missed_rect, "Missed", missed, (210, 120, 110))

        self.draw_results_buttons(shell_rect)

    def draw_score_card(self, rect, score):
        radius = 22

        pygame.draw.rect(self.screen, self.c("surface_shadow"), rect.move(0, 5), border_radius=radius)
        pygame.draw.rect(self.screen, self.c("surface"), rect, border_radius=radius)
        pygame.draw.rect(self.screen, self.c("border"), rect, width=1, border_radius=radius)

        label_surf = self.fonts["small"].render("Overall Score", True, self.c("text_subtle"))
        self.screen.blit(label_surf, (rect.x + 24, rect.y + 22))

        score_text = f"{int(round(score))}%"
        score_surf = self.fonts["hero"].render(score_text, True, self.c("text"))
        self.screen.blit(score_surf, (rect.x + 24, rect.y + 58))
    

    def draw_results_list_card(self, rect, title, items, accent_color):
        radius = 22

        pygame.draw.rect(self.screen, self.c("surface_shadow"), rect.move(0, 5), border_radius=radius)
        pygame.draw.rect(self.screen, self.c("surface"), rect, border_radius=radius)
        pygame.draw.rect(self.screen, self.c("border"), rect, width=1, border_radius=radius)

        title_surf = self.fonts["medium"].render(title, True, self.c("text"))
        self.screen.blit(title_surf, (rect.x + 22, rect.y + 20))

        start_y = rect.y + 72
        row_gap = 32

        if not items:
            empty_surf = self.fonts["small"].render("None", True, self.c("text_faint"))
            self.screen.blit(empty_surf, (rect.x + 22, start_y))
            return

        for i, item in enumerate(items):
            row_y = start_y + i * row_gap

            pygame.draw.circle(self.screen, self.c("chip"), (rect.x + 28, row_y + 8), 8)
            pygame.draw.circle(self.screen, accent_color, (rect.x + 28, row_y + 8), 4)

            label = self.better_pose_naming(item)
            item_surf = self.fonts["small"].render(label, True, self.c("text_soft"))
            self.screen.blit(item_surf, (rect.x + 44, row_y))
    
    def draw_results_buttons(self, shell_rect):
        mouse_pos = pygame.mouse.get_pos()
        speed = 0.30

        primary_fill = self.c("accent")
        primary_hover = self.c("accent_hover")
        primary_text = self.c("text")

        secondary_fill = self.c("shell")
        secondary_hover_fill = self.c("surface_hover")
        secondary_border = self.c("border_strong")
        secondary_hover_border = self.c("border_hover")
        secondary_text = self.c("text_soft")

        y = shell_rect.bottom - 92
        x = shell_rect.right - 430

        retry_base = pygame.Rect(x, y, 180, 50)
        back_base = pygame.Rect(x + 200, y, 180, 50)

        retry_hovered = retry_base.collidepoint(mouse_pos)
        back_hovered = back_base.collidepoint(mouse_pos)

        self.retry_hover_t += ((1.0 if retry_hovered else 0.0) - self.retry_hover_t) * speed
        self.results_back_hover_t += ((1.0 if back_hovered else 0.0) - self.results_back_hover_t) * speed

        retry_lift = int(round(2 * self.retry_hover_t))
        back_lift = int(round(2 * self.results_back_hover_t))

        retry_rect = retry_base.move(0, -retry_lift)
        back_rect = back_base.move(0, -back_lift)

        self.retry_button_rect = retry_rect
        self.results_back_button_rect = back_rect

        retry_fill = self.lerp_color(primary_fill, primary_hover, self.retry_hover_t)
        back_fill = self.lerp_color(secondary_fill, secondary_hover_fill, self.results_back_hover_t)
        back_border = self.lerp_color(secondary_border, secondary_hover_border, self.results_back_hover_t)

        pygame.draw.rect(self.screen, self.c("surface_shadow"), retry_rect.move(0, 4), border_radius=14)
        pygame.draw.rect(self.screen, retry_fill, retry_rect, border_radius=14)

        retry_surf = self.fonts["small"].render("Retry Scenario", True, primary_text)
        self.screen.blit(retry_surf, retry_surf.get_rect(center=retry_rect.center))

        pygame.draw.rect(self.screen, self.c("surface_shadow"), back_rect.move(0, 4), border_radius=14)
        pygame.draw.rect(self.screen, back_fill, back_rect, border_radius=14)
        pygame.draw.rect(self.screen, back_border, back_rect, width=1, border_radius=14)

        back_surf = self.fonts["small"].render("Back to Scenarios", True, secondary_text)
        self.screen.blit(back_surf, back_surf.get_rect(center=back_rect.center))
    

    def get_results_click_target(self, mouse_pos):
        if self.retry_button_rect and self.retry_button_rect.collidepoint(mouse_pos):
            return "retry_scenario"

        if self.results_back_button_rect and self.results_back_button_rect.collidepoint(mouse_pos):
            return "back_to_scenarios"

        return None