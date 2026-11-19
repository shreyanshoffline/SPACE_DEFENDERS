import pygame
from utils import settings
from assets.imgs import checkpoint_img, checkpoint_2_img

class Checkpoint:
    def __init__(self, x, y, wave_number):
        self.x = x
        self.y = y
        self.wave_number = wave_number
        self.img = checkpoint_img
        self.img2 = checkpoint_2_img
        self.activated = False

    def draw(self, win):
        img_to_draw = self.img2 if self.activated else self.img
        win.blit(img_to_draw, (self.x, self.y))

    def collides_with_player(self, player):
        checkpoint_rect = self.img.get_rect(topleft=(self.x, self.y))
        player_rect = player.img.get_rect(topleft=(player.x, player.y))
        return checkpoint_rect.colliderect(player_rect)

    def activate(self, player):
        if not self.activated and self.collides_with_player(player):
            self.activated = True
            player.checkpoint_wave = self.wave_number
