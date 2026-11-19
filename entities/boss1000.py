
import random
import pygame
import time
from utils import settings
from assets.imgs import boss1000_img
from assets.imgs import boss1000_2_img
from assets.imgs import icesuper_img
from entities.enemy import Enemy
from entities.defender import Defender

def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5


# --- Boss1000 Class ---
class Boss1000: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 1500
        self.max_hp = 1500
        self.enraged = False
        self.enraged_speed = 4
        self.img = boss1000_img
        self.img2 = boss1000_2_img
        self.center = (self.x + self.img.get_width() // 2, self.y + self.img.get_height() // 2)
        self.center2 = (self.x + self.img2.get_width() // 2, self.y + self.img2.get_height() // 2)

        self.fallspeed = 8  # Lower speed for smoother drop
        self.speed = 2
        self.name = "Mimic Mayhem"
        self.alive = True
        self.direction = "right" # Initial direction for bouncing
        
        self.enraged_announced = False  # Only announce once
        self.enraged_timer = 0  # For special attacks
        self.special_attack_cooldown = 5  # seconds
        self.last_special_attack = 0

        self.shockwave_active = False
        self.shockwave_radius = 0
        self.shockwave_max_radius = 100000  # Set to a very large value to avoid premature deactivation
        self.shockwave_cooldown = 8
        self.last_shockwave_time = 0



    def draw(self, win):
        # Only draw if alive and hp > 0
        if not self.alive or self.hp <= 1:
            return
        # Always use img2 if enraged, otherwise img
        if self.enraged:
            win.blit(self.img2, (self.x, self.y))
            bar_x = self.x + self.img2.get_width() // 2 - 200
            bar_y = self.y - 40
            draw_health_bar(win, bar_x, bar_y, max(0, self.hp), 500, "Enraged Mimic Mayhem")
            # Announce enraged state once
            if not self.enraged_announced:
                font = pygame.font.SysFont("comicsans", 40)
                text = font.render("MIMIC MAYHEM IS ENRAGED!", True, (255, 100, 0))
                win.blit(text, (settings.WIN_WIDTH // 2 - text.get_width() // 2, 60))
                self.enraged_announced = True
            if self.shockwave_active:
                pygame.draw.circle(win, (255, 0, 0), self.center2, self.shockwave_radius, 2)
        else:
            win.blit(self.img, (self.x, self.y))
            bar_x = self.x + self.img.get_width() // 2 - 200
            bar_y = self.y - 40
            draw_health_bar(win, bar_x, bar_y, max(0, self.hp - 500), 1000, self.name)

    def update(self):
        # Transition to enraged state
        if self.hp <= 500 and not self.enraged and self.alive and self.hp > 0:
            self.enraged = True
            self.enraged_announced = False  # Reset for draw
            self.last_special_attack = pygame.time.get_ticks() / 1000
        # Special attack logic (enraged only)
        if self.enraged and self.alive and self.hp > 0:
            now = pygame.time.get_ticks() / 1000
            if self.shockwave_active:
                pygame.draw.circle(settings.WIN, (0, 255, 255), (self.x + self.img.get_width()//2, self.y + self.img.get_height()//2), self.shockwave_radius, 3)
        if self.enraged and not self.shockwave_active and self.shockwave_cooldown <= 0 and self.alive:
            self.shockwave_active = True
            self.shockwave_radius = 0
            self.shockwave_cooldown = 600  # frames until next attack (10 sec at 60 FPS)
        

    def move(self):
        if self.alive and self.hp > 0:
            # First: descend from the top
            if self.y < 75:
                self.y += self.fallspeed  # boss drops down into position

            elif self.y >= 75:
                if self.direction == "right":
                    if self.enraged:
                        self.x += self.enraged_speed
                    else:
                        self.x += self.speed
                    if self.x >= settings.WIN_WIDTH - self.img.get_width() - 100:
                        self.direction = "left"

                else:  # self.direction == "left"
                    if self.enraged:
                        self.x -= self.enraged_speed
                    else:
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

        if self.enraged:
            self.hp -= int(damage * 0.7)  # Enraged takes reduced damage
        else:
            self.hp -= damage

        if self.hp <= 1:
            self.hp = 0
            self.alive = False
            self.enraged = False  # Shut off any future attacks
            self = 0

    def trigger_shockwave(self):
        if self.alive and self.hp > 0:
            if not self.enraged:
                return

            current_time = time.time()
            if current_time - self.last_shockwave_time > self.shockwave_cooldown:
                self.shockwave_active = True
                self.shockwave_radius = 0
                self.last_shockwave_time = current_time

    def update_shockwave(self, defender, enemies, super_lasers):
        if not self.shockwave_active:
            return

        self.shockwave_radius += 5  # Expand speed (you can tweak this)

        boss_center = (
            self.x + self.img.get_width() // 2,
            self.y + self.img.get_height() // 2
        )

        def is_blocked():
            for enemy in enemies:
                if enemy.alive and distance((enemy.x, enemy.y), boss_center) < self.shockwave_radius:
                    return True
            for laser in super_lasers:
                if getattr(laser, "frozen", False) and distance((laser.x, laser.y), boss_center) < self.shockwave_radius:
                    return True
            return False

        dist_to_def = distance((defender.x + defender.img.get_width()//2, defender.y + defender.img.get_height()//2), boss_center)

        if dist_to_def <= self.shockwave_radius and not is_blocked():
            defender.hp = 0  # Insta-kill

        if self.shockwave_radius > self.shockwave_max_radius:
            self.shockwave_active = False



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
        if num <= 4 and not self.enraged:  # 40% chance to freeze boss1000      
            for laser in super_lasers:
                laser.frozen = True
                laser.img = icesuper_img  # change appearance
        if self.enraged:
            n = random.randint(1, 10)
            if n <= 6:
                for laser in super_lasers:
                    laser.frozen = True
                    laser.img = icesuper_img  # change appearance
        
            
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
