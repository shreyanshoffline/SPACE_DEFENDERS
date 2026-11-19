import pygame
from utils import settings
from assets.imgs import meteor_img, meteor_2_img


class Meteor:
    def __init__(self, x, y, is_reflectable=False):
        self.x = x
        self.y = y
        self.vel = 4
        self.is_reflectable = is_reflectable
        self.width = 30  # example size
        self.height = 30
        self.img = meteor_img
        self.img2 = meteor_2_img
        self.damage = 100
        # maybe add image or color here

    def update(self):
        self.y += self.vel  # meteor falls down

    def draw(self, win):
        img = self.img2 if self.is_reflectable else self.img
        win.blit(img, (self.x, self.y))  # Placeholder for actual image

    def off_screen(self, height):
        return self.y > height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
