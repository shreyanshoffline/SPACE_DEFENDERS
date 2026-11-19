import pygame
import sys
import time

from utils import settings
from utils import collision as colli
from screens.start_screen import start_screen
from entities.defender import Defender
from entities.laser import Laser
from entities.boss500 import Boss500
from entities.boss1000 import Boss1000
from entities.knight import Knight
from entities.meteor import Meteor
from entities.checkpoint import Checkpoint
from entities.boss2500 import Boss2500
from entities import enemy as enmy
from assets.imgs import bg_img, boss500_img, boss1000_img, knight_img, boss2500_img

pygame.init()
WIN = pygame.display.set_mode((settings.WIN_WIDTH, settings.WIN_HEIGHT))
pygame.display.set_caption("🚀 SPACE DEFENDERS !!!")


def main(screen):
    # Game state variables
    clock = pygame.time.Clock()
    run = True
    game_over = False

    # Timing and cooldowns
    last_shot_time = 0
    shoot_delay = 0.25
    reload_time = 3
    reload_start_time = 0
    laser_limit = 50
    laser_count = 0
    reloading = False

    # Player and progression
    player = Defender(500, 750)
    super_damadge = 200
    super_ready = False
    total_damage_dealt = 0
    enemy_kills = 0
    wave_count = player.checkpoint_wave or 0

    # Entities and objects
    lasers, super_lasers = [], []
    enemies, meteors = [], []
    boss500 = boss1000 = knight = boss2500 = None
    boss500_defeated = boss1000_defeated = knight_defeated = boss2500_defeated = False

    checkpoint = None
    checkpoint_spawned = False
    checkpoint_activated_time = None
    last_clone_time = 0
    meteor_timer = 0

    start_screen(screen, player.img, bg_img)

    while run:
        current_time = time.time()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Wave Spawning ---
        bosses_dead = all(
            boss is None or not boss.alive for boss in [boss500, boss1000, knight, boss2500]
        )
        if not enemies and (bosses_dead or (checkpoint and checkpoint.activated)):
            enmy.spawn_enemy_wave(enemies)
            wave_count += 1

        # --- Enemy Movement ---
        for enemy in enemies:
            enemy.move()
        enemies = [e for e in enemies if not e.off_screen()]

        # --- Boss Triggers ---
        if wave_count == 5 and boss500 is None and not boss500_defeated:
            boss500 = Boss500(settings.WIN_WIDTH // 2 - boss500_img.get_width() // 2, -150)

        if wave_count == 10 and boss1000 is None and not boss1000_defeated:
            boss1000 = Boss1000(settings.WIN_WIDTH // 2 - boss1000_img.get_width() // 2, -150)

        if wave_count == 15 and knight is None and not knight_defeated:
            knight = Knight(settings.WIN_WIDTH // 2 - knight_img.get_width() // 2, -150)

        if wave_count == 20 and boss2500 is None and not boss2500_defeated:
            boss2500 = Boss2500(settings.WIN_WIDTH // 2 - boss2500_img.get_width() // 2, -150)

        # --- Checkpoint Setup ---
        if wave_count in [11, 21] and not checkpoint_spawned:
            checkpoint = Checkpoint(settings.WIN_WIDTH // 2 - 32, settings.WIN_HEIGHT - 100, wave_count)
            checkpoint_spawned = True

        if checkpoint:
            if checkpoint.collides_with_player(player):
                checkpoint.activate(player)
                checkpoint_activated_time = current_time
                print(f"Checkpoint activated at wave {wave_count}")

        # TODO: Add logic for shooting, collisions, drawing, etc.

        # --- Drawing ---
        WIN.blit(bg_img, (0, 0))
        player.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)
        for laser in lasers:
            laser.draw(WIN)
        for sl in super_lasers:
            sl.draw(WIN)
        if checkpoint:
            checkpoint.draw(WIN)

        pygame.display.update()

if __name__ == "__main__":
    main(WIN)

