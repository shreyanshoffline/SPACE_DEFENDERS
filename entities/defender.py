import pygame
from utils import settings
import time
from assets.imgs import defender_img, super_img

class Defender:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = defender_img
        self.vel = 8 # Speed of the defender
        self.hp = 100
        self.shield = 100
        self.regen_shield = 50
        self.checkpoint_wave = 1
        
        self.last_hit_time = time.time()

    def regenerate_shield(self):
        if time.time() - self.last_hit_time > 3:
            self.regen_shield = min(self.regen_shield + 0.15, 50)



    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        self.draw_health_bar(settings.WIN)

                
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x < settings.WIN_WIDTH - self.img.get_width():
            self.x += self.vel
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y < settings.WIN_HEIGHT - self.img.get_height():
            self.y += self.vel

    def get_gun_positions(self, super_laser=False):
        if super_laser:
            # grab the super laser’s true width & height
            sw, sh = super_img.get_size()

            # center it horizontally on the ship
            x = self.x + (self.img.get_width() - sw) // 2

            # fire it from just above the ship’s top edge (tweak the -sh//2 or -sh+10 as desired)
            y = self.y - sh 

            return x, y

        else:
            left = self.x + 12
            right = self.x + self.img.get_width() - 18
            y = self.y + 5
            return (left, y), (right, y)
        
    def draw_health_bar(self, win):
        # Bar sizes
        bar_width = 300   # bigger horizontal bars
        bar_height = 25   # taller for visibility
        spacing = 10      # space between bars
        margin = 30       # distance from screen edge

        # Bottom-left position
        x = margin
        y = settings.WIN_HEIGHT - margin - (bar_height * 2 + spacing)

        # --- GREEN: Health ---
        hp_ratio = self.hp / 100
        pygame.draw.rect(win, (40, 40, 40), (x, y + bar_height + spacing, bar_width, bar_height))  # background
        pygame.draw.rect(win, (0, 255, 0), (x, y + bar_height + spacing, bar_width * hp_ratio, bar_height))  # filled

        # --- BLUE: Shield ---
        shield_ratio = min(self.shield, 100) / 100
        pygame.draw.rect(win, (40, 40, 40), (x, y, bar_width, bar_height))  # background
        pygame.draw.rect(win, (0, 150, 255), (x, y, bar_width * shield_ratio, bar_height))  # filled

        # --- CYAN: Regen Shield (Vertical bar next to the others) ---
        regen_ratio = min(self.regen_shield, 50) / 50
        regen_bar_height = bar_height * 2 + spacing
        regen_bar_width = 18  # wider than before
        regen_x = x + bar_width + 15  # space between bars
        regen_y = y + (regen_bar_height * (1 - regen_ratio))
        filled_height = regen_bar_height * regen_ratio

        pygame.draw.rect(win, (40, 40, 40), (regen_x, y, regen_bar_width, regen_bar_height))  # background
        pygame.draw.rect(win, (0, 255, 255), (regen_x, regen_y, regen_bar_width, filled_height))  # filled



    def take_damage(self, dmg):
        self.last_hit_time = time.time()

        # Regen shield takes damage first
        if self.regen_shield > 0:
            absorb = min(dmg, self.regen_shield)
            self.regen_shield -= absorb
            dmg -= absorb

        # Then shield
        if dmg > 0 and self.shield > 0:
            absorb = min(dmg, self.shield)
            self.shield -= absorb
            dmg -= absorb
        # Then HP
        if dmg > 0:
            self.hp -= dmg
        
        if self.hp <= 0:
            self.hp = 0
            self.alive = False



                
