
import random
import pygame
from utils import settings
from assets.imgs import knight_img
from entities.enemy import Enemy

# --- Boss500 Class ---
class Knight: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 750
        self.max_hp = 750
        self.img = knight_img
        self.fallspeed = 10  # Lower speed for smoother drop
        self.speed = 3
        self.name = "The Evil Knight"
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
            # Steep Zig-Zag V — enemies zip in like lightning bolts ⚡
            [(-180, 150), (-90, 100), (-60, 130), (-30, 90), (0, 60), (30, 90), (60, 130), (90, 100), (180, 150)],

            # Split-Tip V — enemy group splits at bottom tip, like a double tail 👿
            [(-160, 140), (-80, 120), (-40, 100), (0, 80), (20, 60), (40, 80), (80, 100), (160, 140)],

            # Deep Cut V — super narrow and drops way lower to surprise the player 👇
            [(-100, 120), (-60, 100), (-30, 80), (0, 40), (30, 80), (60, 100), (100, 120)],

            # Wave-V Combo — mixes a V shape with sine wave points 🌊🔻
            [(-160, 160), (-120, 140), (-80, 150), (-40, 130), (0, 90), (40, 130), (80, 150), (120, 140), (160, 160)]
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
    
    

