import pygame
from utils import settings
from assets.imgs import laser_img, super_img
# --- Laser Class ---
class Laser:
    def __init__(self, x, y, damage=5, super_laser=False):
        self.x = x
        self.y = y
        self.frozen = False
        self.damage = damage
        self.remaining_damage = damage
        self.super_laser = super_laser
        self.img = laser_img if not super_laser else super_img
        self.vel = -12 if not super_laser else -6  # super lasers move slower but hit harder

        if super_laser:
            self.remaining_damage = 250  # Super laser's total damage pool
        else:
            self.remaining_damage = damage


    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self):
        if self.frozen:
            self.y -= 0.1
        else: 
            self.y += self.vel

    def off_screen(self):
        return self.y < -self.img.get_height()
