import pygame
import time
import random
from assets.imgs import laser_beam_img
from utils import settings

class LaserBeam:
    def __init__(self, win_width, win_height):
        self.win_width = win_width
        self.win_height = win_height
        self.img = laser_beam_img
        self.img_width = self.x + self.img.get_width()

        # Pick random side + position
        self.side = random.randint(1, 2)
        self.y = (win_height // 2) + 50

        if self.side == 1:
            self.x = 0
            self.width = random.randint(win_width // 3, (win_width // 3) * 2)
        else:
            self.x = random.randint(win_width // 3, (win_width // 3) * 2)
            self.width = win_width - self.x

        self.height = win_height - self.y
        self.warning_duration = 1  # seconds before firing
        self.start_time = time.time()
        self.firing = False
        self.active = True
        self.vel = 12  # only needed if beam scrolls
        self.damage = 250

    def update(self, win):
        elapsed = time.time() - self.start_time
        if elapsed < self.warning_duration:
            # --- Warning phase ---
            transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(transparent_surface, (255, 0, 0, 128), (0, 0, self.width, self.height))
            win.blit(transparent_surface, (self.x, self.y))
        else:
            # --- Firing phase ---
            self.firing = True
            win.blit(self.img, (self.x, self.y))

    def move(self):
        # Only move if needed
        if self.firing:
            self.x += self.vel
            self.img_width += self.vel

            if self.img_width > self.width:
                self.active = False
