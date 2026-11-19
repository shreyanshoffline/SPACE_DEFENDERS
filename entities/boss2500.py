
import random
import pygame
import time
from utils import settings
from assets.imgs import boss2500_img
from assets.imgs import icesuper_img
from entities.enemy import Enemy
from entities.defender import Defender

# --- Boss2500 Class ---
class Boss2500: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 2500
        self.max_hp = 2500
        self.img = boss2500_img
        self.center = (self.x + self.img.get_width() // 2, self.y + self.img.get_height() // 2)

        self.fallspeed = 6  # Lower speed for smoother drop
        self.speed = 4
        self.name = "COLOSSAL CYBORG"
        self.alive = True
        self.direction = "right" # Initial direction for bouncing

    def draw(self, win):
        # Only draw if alive and hp > 0
        if self:
            if not self.alive or self.hp <= 1:
                return
            win.blit(self.img, (self.x, self.y))
            draw_health_bar(win, self, self.hp, self.max_hp, "THE COLOSSAL CYBORG!")
        else:
            return

    def move(self):
        if self.alive and self.hp > 0:
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
        else:
            self = 0  # Remove boss if not alive
            return

    def hit(self, damage):
        if not self.alive:
            return

        self.hp -= damage

        if self.hp <= 1:
            self.hp = 0
            self.alive = False
            self = 0

    def off_screen(self):
        return self.y > settings.WIN_HEIGHT

    def spawn_clones(self, enemy_list):
        v_patterns = [
    # 💀 Aggressive Steep V
    [(-60, 200), (-40, 150), (-20, 100), (0, 70), (20, 100), (40, 150), (60, 200)],

    # 💥 Offset Zigzag V
    [(-160, 150), (-120, 120), (-80, 100), (-40, 90), (0, 85),
     (40, 90), (80, 100), (120, 120), (160, 150)],

    # 🔀 Criss-Cross X-V
    [(-100, 120), (-50, 100), (0, 80), (50, 100), (100, 120),
     (-50, 140), (0, 120), (50, 140)],

    # 🌀 Spiral V Formation
    [(-90, 100), (-30, 80), (0, 60), (30, 80), (90, 100),
     (-60, 130), (0, 110), (60, 130),
     (-30, 160), (30, 160)],

    # 🪬 Inverted Reverse V
    [(0, 60), (-30, 80), (-60, 100), (-90, 130),
     (0, 60), (30, 80), (60, 100), (90, 130)],
]


        selected_pattern = random.choice(v_patterns)

        for dx, dy in selected_pattern:
            x = self.x + dx
            y = self.y + dy
            if 0 <= x <= settings.WIN_WIDTH - 64:
                enemy_list.append(Enemy(x, y))
            
    def freeze(self, super_lasers):
        # Only freeze if alive
        if not self.alive:
            return
        # Frozen lasers have a chance to freeze the boss (visual effect only)
        num = random.randint(1, 10)
        if num <= 6:  # 60% chance to freeze boss2500      
            for laser in super_lasers:
                laser.frozen = True
                laser.img = icesuper_img  # change appearance        
            
    def get_rect(self):
        current_img = self.img2 if hasattr(self, "enraged") and self.enraged else self.img
        return current_img.get_rect(topleft=(self.x, self.y))
    
def draw_health_bar(win, boss, hp, max_hp, title):
    """
    Draws a boss health bar above the boss's head, scaled to its sprite width.
    Has a gradient color effect for final boss flair.
    """
    font = pygame.font.SysFont("comicsans", 30)
    title_text = font.render(title, True, (255, 255, 255))

    # Bar size relative to boss sprite
    bar_width = boss.img.get_width()
    bar_height = 20
    x = boss.x
    y = boss.y - 30  # Above boss

    # Draw outline
    pygame.draw.rect(win, (255, 255, 255), (x, y, bar_width, bar_height), 2)

    # Prevent negative width
    hp = max(0, min(hp, max_hp))
    fill_width = int((hp / max_hp) * bar_width)

    # Gradient: Green → Yellow → Orange → Red
    health_ratio = hp / max_hp
    if health_ratio > 0.75:
        color = (0, 255, 0)
    elif health_ratio > 0.5:
        color = (255, 215, 0)
    elif health_ratio > 0.25:
        color = (255, 140, 0)
    else:
        color = (255, 0, 0)

    # Draw filled bar
    pygame.draw.rect(win, color, (x, y, fill_width, bar_height))

    # Draw title above bar
    win.blit(title_text, (x + bar_width // 2 - title_text.get_width() // 2, y - 25))
