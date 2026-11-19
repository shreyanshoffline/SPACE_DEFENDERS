import pygame
import random
from utils import settings

# --- Assets ---
# --- Load Images ---
# Defender

defender_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/defender.png").convert_alpha()
defender_img = pygame.transform.scale(defender_img, (64, 64))
# Boss artillery
laser_beam_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/laser_beam.png").convert_alpha()
laser_beam_img = pygame.transform.scale(laser_beam_img, (400,400))

meteor_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/meteor.png").convert_alpha()
meteor_img = pygame.transform.scale(meteor_img, (100, 100))
meteor_2_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/meteor_2.png").convert_alpha()
meteor_2_img = pygame.transform.scale(meteor_2_img, (100, 100))
# Enemies
enemy_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (64, 64))

knight_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/knight.png").convert_alpha()
knight_img = pygame.transform.scale(knight_img, (316, 316))
# Bosses
boss500_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/boss500.png").convert_alpha()
boss500_img = pygame.transform.scale(boss500_img, (284, 284))  # or even bigger

boss1000_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/boss1000.png").convert_alpha()
boss1000_img = pygame.transform.scale(boss1000_img, (364, 364))
boss1000_2_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/boss1000_phase2.png").convert_alpha()
boss1000_2_img = pygame.transform.scale(boss1000_2_img, (384, 384))  # or even bigger

boss2500_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/boss2500.png").convert_alpha()
boss2500_img = pygame.transform.scale(boss2500_img, (436, 436))  # or even bigger

# Bg
bg_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/bg.png").convert_alpha()
bg_img = pygame.transform.scale(bg_img, (settings.WIN_WIDTH, settings.WIN_HEIGHT))  # or even bigger

# Lasers
laser_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/laser.png").convert_alpha()
laser_img = pygame.transform.scale_by(laser_img, 0.02)
# Supers
super_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/super_laser.png").convert_alpha()
super_img = pygame.transform.scale_by(super_img, 0.50)  # Scale to visible size!
icesuper_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/super_laser_ice.png").convert_alpha()
icesuper_img = pygame.transform.scale_by(icesuper_img, 0.50)  # Scale to visible size!

# Extra imgs
checkpoint_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/checkpoint.png").convert_alpha()
checkpoint_img = pygame.transform.scale(checkpoint_img, (128, 128))

checkpoint_2_img = pygame.image.load("SPACE_DEFENDERS/assets/Space_imgs/checkpoint_2.png").convert_alpha()
checkpoint_2_img = pygame.transform.scale(checkpoint_2_img, (136, 136))