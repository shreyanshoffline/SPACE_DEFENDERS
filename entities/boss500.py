
import random
import pygame
from utils import settings
from assets.imgs import boss500_img
from entities.enemy import Enemy

# --- Boss500 Class ---
class Boss500: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 500
        self.max_hp = 500
        self.img = boss500_img
        self.fallspeed = 10  # Lower speed for smoother drop
        self.speed = 3
        self.name = "Tentacle Terror"
        self.alive = True
        self.direction = "right" # Initial direction for bouncing

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        # Draw health bar above the boss
        bar_x = self.x + self.img.get_width() // 2 - 200  # Center the bar above the boss
        bar_y = self.y - 40  # Above the boss image
        draw_health_bar(win, bar_x, bar_y, self.hp, self.max_hp, self.name)

    def move(self):
        # First: descend from the top
        if self.y < 75:
            self.y += self.fallspeed  # boss drops down into position

        elif self.y >= 75:
            if self.direction == "right":
                self.x += self.speed
                if self.x >= settings.WIN_WIDTH - self.img.get_width() - 100:
                    self.direction = "left"

            else:  # self.direction == "left"
                self.x -= self.speed
                if self.x <= 100:
                    self.direction = "right"
        # Once settled, bounce horizontally

    def hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def off_screen(self):
        return self.y > settings.WIN_HEIGHT

    def spawn_clones(self, enemy_list):
        v_patterns = [
            # Classic wide V
            [(-150, 150), (-100, 120), (-50, 100), (0, 80), (50, 100), (100, 120), (150, 150)],
            
            # Sharper V
            [(-100, 130), (-60, 100), (-30, 80), (0, 60), (30, 80), (60, 100), (100, 130)],
            
            # Flat base V
            [(-200, 170), (-100, 140), (0, 110), (100, 140), (200, 170)],
            
            # Nested V (Double Layer)
            [(-120, 130), (-80, 110), (-40, 90), (0, 70), (40, 90), (80, 110), (120, 130),
            (-60, 160), (0, 140), (60, 160)]
        ]

        selected_pattern = random.choice(v_patterns)

        for dx, dy in selected_pattern:
            x = self.x + dx
            y = self.y + dy
            if 0 <= x <= settings.WIN_WIDTH - 64:
                enemy_list.append(Enemy(x, y))
                
    def get_rect(self):
        current_img = self.img2 if hasattr(self, "enraged") and self.enraged else self.img
        return current_img.get_rect(topleft=(self.x, self.y))




# --- Draw Health Bar ---
def draw_health_bar(win, x, y, hp, max_hp, title):
    # Fonts
    font = pygame.font.SysFont("comicsans", 30)
    title_text = font.render(title, True, (255, 255, 255))
    
    # Bar outline
    bar_width = 400
    bar_height = 25
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    pygame.draw.rect(win, (255, 255, 255), outline_rect, 2)

    # Health fill
    fill_width = int((hp / max_hp) * bar_width)
    fill_rect = pygame.Rect(x, y, fill_width, bar_height)

    # Color logic: Green → Yellow → Red
    if hp / max_hp > 0.6:
        color = (0, 255, 0)
    elif hp / max_hp > 0.3:
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)

    pygame.draw.rect(win, color, fill_rect)
    win.blit(title_text, (x + 200, y - 25))  # Adjusted y position for better visibility
    
    

