import pygame
from utils import settings
import random
from assets.imgs import enemy_img

# --- Enemy Class ---
class Enemy:
    def __init__(self, x=None, y=None):
        self.img = enemy_img
        self.vel = 2
        self.health = 5
        self.alive = True
        self.rect = self.img.get_rect()


        # If x or y aren't given, use random values
        self.x = x if x is not None else random.randint(0, settings.WIN_WIDTH - self.rect.width)
        self.y = y if y is not None else random.randint(-100, -40)


    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += self.vel

    def off_screen(self):
        return self.y > settings.WIN_HEIGHT

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False



# --- Enemy Patterns ---
enemy_patterns = [
    [(200, -60), (350, -60), (500, -60), (650, -60), (800, -60)],
    [(500, -60), (400, -130), (600, -130), (300, -200), (700, -200)],
    [(300, -60), (400, -120), (500, -60), (600, -120), (700, -60)],
    [(500, -200), (400, -130), (600, -130), (300, -260), (700, -260)],
    [(500, -60), (500, -180), (380, -120), (620, -120), (260, -150), (740, -150)],
    [(200, -60), (300, -100), (400, -140), (500, -180), (600, -220), (700, -260)],
    [(500, -60), (440, -120), (560, -120), (380, -180), (620, -180), (320, -240), (680, -240)],
    [(300, -200), (400, -150), (500, -120), (600, -150), (700, -200)],
]


# --- Function to spawn enemies ---
def spawn_enemy_wave(enemy_list):
    pattern = random.choice(enemy_patterns)
    for x, y in pattern:
        enemy_list.append(Enemy(x, y))