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
    game_over = False
    restart_rect = None

    last_shot_time = 0
    shoot_delay = 0.25
    reload_time = 3
    laser_limit = 50
    laser_count = 0
    reloading = False
    reload_start_time = 0
    super_damadge = 200

    run = True
    clock = pygame.time.Clock()
    player = Defender(500, 750)
    
    boss500 = None
    boss1000 = None
    boss2500 = None
    knight = None
    boss500_defeated = False
    boss1000_defeated = False
    knight_defeated = False
    boss2500_defeated = False

    checkpoint = None
    checkpoint_spawned = False
    checkpoint_activated_time = None

    lasers = []
    super_lasers = []
    enemies = []
    meteors = []

    super_ready = False
    enemy_kills = 0
    total_damage_dealt = 0

    last_clone_time = 0
    meteor_timer = 0
    wave_count = 0

    start_screen(screen, player.img, bg_img)
    while run:
        current_time = time.time()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        # Allow enemy waves to spawn if no enemies and (no bosses alive or after checkpoint)
        bosses_dead = (boss500 is None or not boss500.alive) and (boss1000 is None or not boss1000.alive) and (knight is None or not knight.alive) and (boss2500 is None or not boss2500.alive)
        if (len(enemies) == 0) and (bosses_dead or (checkpoint and checkpoint.activated)):
            enmy.spawn_enemy_wave(enemies)
            wave_count += 1
        for enemy in enemies:
            enemy.move()
        enemies = [e for e in enemies if not e.off_screen()]

        # Boss500 Setup
        if wave_count == 5 and boss500 is None and not boss500_defeated:
            boss500_x = settings.WIN_WIDTH // 2 - boss500_img.get_width() // 2
            boss500_y = -150
            boss500 = Boss500(boss500_x, boss500_y)

        # Boss1000 Setup
        if wave_count == 10 and boss1000 is None and not knight_defeated:
            boss1000_x = settings.WIN_WIDTH // 2 - boss1000_img.get_width() // 2
            boss1000_y = -150
            boss1000 = Boss1000(boss1000_x, boss1000_y)

        # Knight Setup
        if wave_count == 15 and knight is None and not boss1000_defeated:
            knight_x = settings.WIN_WIDTH // 2 - knight_img.get_width() // 2
            knight_y = -150
            knight = Knight(knight_x, knight_y)

        # Boss2500 Setup
        if wave_count == 20 and boss2500 is None and not boss2500_defeated:
            boss2500_x = settings.WIN_WIDTH // 2 - boss2500_img.get_width() // 2
            boss2500_y = -200
            boss2500 = Boss2500(boss2500_x, boss2500_y)
        if boss2500 and boss2500.alive:
            # === BOSS2500 Meteor Firing ===
            meteor_timer += 1
            if meteor_timer >= 160:  # every 90 frames (adjust as needed)
                import random
                meteor_x = boss2500.x + boss2500.y // 2 - 15  # center meteor
                is_reflectable = random.randint(1, 4) == 1  # 1 in 4 chance
                new_meteor = Meteor(meteor_x, boss2500.y + boss2500.x, is_reflectable)
                meteors.append(new_meteor)
                meteor_timer = 0

        # (Removed pre-collision boss move/draw logic. Bosses are now only moved/drawn after collision and alive state update.)

        keys = pygame.key.get_pressed()
        player.move(keys)

        if reloading and current_time - reload_start_time >= reload_time:
            reloading = False
            laser_count = 0
        elif keys[pygame.K_SPACE] and current_time - last_shot_time >= shoot_delay:
            (lx, ly), (rx, ry) = player.get_gun_positions(super_laser=False)
            lasers.extend([Laser(lx, ly), Laser(rx, ry)])
            last_shot_time = current_time
            laser_count += 1
            if laser_count >= laser_limit:
                reloading = True
                reload_start_time = current_time
        elif keys[pygame.K_b] and current_time - last_shot_time >= shoot_delay and super_ready:
            x, y = player.get_gun_positions(super_ready)
            super_lasers.append(Laser(x, y, super_damadge, super_ready))
            last_shot_time = current_time
            super_ready = False
            if boss1000 and boss1000.alive:
                boss1000.freeze(super_lasers)

        for laser in lasers:
            laser.move()
        lasers = [l for l in lasers if not l.off_screen()]
        for s_laser in super_lasers:
            s_laser.move()
        super_lasers = [l for l in super_lasers if not l.off_screen()]

        # --- COLLISION AND BOSS ALIVE STATE UPDATE ---
        colli.handle_enemy_defender_collisions(player, enemies, game_over)
        colli.handle_boss_defender_collisions(player, [boss500, knight, boss1000, boss2500], game_over)
        hit_lasers_enemies, super_ready, enemy_kills, total_damage_dealt = colli.handle_laser_enemy_collisions(
            lasers, super_lasers, enemies, super_ready, enemy_kills, total_damage_dealt
        )
        hit_lasers_bosses, bosses_alive = colli.handle_laser_boss_collisions(lasers, super_lasers, [boss500, knight, boss1000, boss2500])
        if boss500:
            boss500.alive = bosses_alive[0]
        if knight:
            knight.alive = bosses_alive[1]
        if boss1000:
            boss1000.alive = bosses_alive[2]
        if boss2500:
            boss2500.alive = bosses_alive[3]
        # Remove all lasers that hit anything
        lasers_to_remove = hit_lasers_enemies + hit_lasers_bosses
        lasers = [l for l in lasers if l not in lasers_to_remove and not l.off_screen()]
        super_lasers = [l for l in super_lasers if l not in lasers_to_remove and l.remaining_damage > 0 and not l.off_screen()]

        # Draw everything
        WIN.blit(bg_img, (0, 0))
        player.draw(WIN)
        player.regenerate_shield()

        for laser in lasers:
            laser.draw(WIN)
        for s_laser in super_lasers:
            s_laser.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)
        for meteor in meteors[:]:
            meteor.update()
            meteor.draw(WIN)

            if meteor.off_screen(settings.WIN_HEIGHT):  # remove if off screen
                meteors.remove(meteor)


        # --- DRAW BOSSES ONLY IF ALIVE (AFTER COLLISION UPDATE) ---
        if boss500 and boss500.alive and not boss500_defeated:
            boss500.move()
            boss500.draw(WIN)
            if boss500.hp <= 1:
                boss500.alive = False
                boss500_defeated = True
        if boss500 and boss500.alive and current_time - last_clone_time > 4:
            boss500.spawn_clones(enemies)
            last_clone_time = current_time

        if knight and knight.alive and not knight_defeated:
            knight.move()
            knight.draw(WIN)
            if knight.hp <= 1:
                knight.alive = False
                knight_defeated = True
        if knight and knight.alive and current_time - last_clone_time > 3:
            knight.spawn_clones(enemies)
            last_clone_time = current_time

        if boss1000 and boss1000.hp <= 1 and boss1000.alive:
            boss1000.alive = False
            boss1000_defeated = True
        if boss1000 and boss1000.alive and not boss1000_defeated:
            boss1000.update()
            boss1000.move()
            boss1000.draw(WIN)
        if boss1000 and boss1000.alive and current_time - last_clone_time > 3:
            boss1000.spawn_clones(enemies)
            last_clone_time = current_time
        if boss1000 and boss1000.alive and boss1000.enraged:
            boss1000.update_shockwave(player, enemies, super_lasers)
            boss1000.trigger_shockwave()

        if boss2500 and boss2500.hp <= 1 and boss2500.alive:
            boss2500.alive = False
            boss2500_defeated = True
        if boss2500 and boss2500.alive and not boss2500_defeated:
            boss2500.move()
            boss2500.draw(WIN)
        if boss2500 and boss2500.alive and current_time - last_clone_time > 3:
            boss2500.spawn_clones(enemies)
            last_clone_time = current_time

        enemies = [e for e in enemies if e.alive and not e.off_screen()]

        if game_over and restart_rect:
            for laser in lasers + super_lasers:
                if restart_rect.collidepoint(laser.x, laser.y):
                    return

        if game_over:
            font = pygame.font.SysFont("comicsans", 60)
            restart_text = font.render("RESTART", True, (255, 0, 0))
            restart_rect = restart_text.get_rect(center=(settings.WIN_WIDTH // 2, settings.WIN_HEIGHT // 2))
            WIN.blit(restart_text, restart_rect)

        if wave_count in [3, 4, 5] and (not boss500 or (boss500 and boss500.alive and boss500.y < 75)) and not boss500_defeated:
            font = pygame.font.SysFont("comicsans", 40)
            warning = font.render("WARNING: Tentacle Terror Approaching!", True, (255, 0, 0))
            WIN.blit(warning, (settings.WIN_WIDTH // 2 - warning.get_width() // 2, 100))

        if wave_count in [8, 9, 10] and (not boss1000 or (boss1000 and boss1000.alive and boss1000.y < 75)) and not boss1000_defeated:
            font = pygame.font.SysFont("comicsans", 40)
            warning = font.render("MAYHEM: The grasp of Mimic Mayhem Approaching!", True, (255, 0, 0))
            WIN.blit(warning, (settings.WIN_WIDTH // 2 - warning.get_width() // 2, 100))


        if wave_count in [13, 14, 15] and (not knight or (knight and knight.alive and knight.y < 75)) and not knight_defeated:
            font = pygame.font.SysFont("comicsans", 40)
            warning = font.render("UPCOMING: The Wrath of The Evil Knight", True, (255, 0, 0))
            WIN.blit(warning, (settings.WIN_WIDTH // 2 - warning.get_width() // 2, 100))

        if wave_count in [18, 19, 20] and (not boss2500 or (boss2500 and boss2500.alive and boss2500.y < 75)) and not boss2500_defeated:
            font = pygame.font.SysFont("comicsans", 40)
            warning = font.render("THE COLOSSAL CYBORG IS APPROACHING!", True, (255, 0, 0))
            WIN.blit(warning, (settings.WIN_WIDTH // 2 - warning.get_width() // 2, 100))
        # (Removed duplicate boss draw calls; bosses are already drawn above after collision update)

        if wave_count > 5 and wave_count < 7 and boss500.hp <= 1 and not boss500.alive and boss500_defeated:
            font = pygame.font.SysFont("comicsans", 20)
            warning = font.render("Congrats on your journey! The Tentacle Terror has finally fallen! You must continue on your epic quest!", True, (144, 238, 144))
            WIN.blit(warning, (settings.WIN_WIDTH // 2 - warning.get_width() // 2, 50))

        if wave_count > 10 and wave_count < 13  and boss1000 and boss1000.hp <= 1 and not boss1000.alive and boss1000_defeated:
            font = pygame.font.SysFont("comicsans", 20)
            warning = font.render("Amazing, Galactic Savior! The Mimic Mayhem's rule has finally fallen! Intergalactic Freedom !", True, (144, 238, 144))
            WIN.blit(warning, (settings.WIN_WIDTH // 2 - warning.get_width() // 2, 50))
                         
        if wave_count > 15 and wave_count < 17 and knight and knight.hp <= 1 and not knight.alive and knight_defeated:
            font = pygame.font.SysFont("comicsans", 20)
            warning = font.render("Your battle stories are echoing and the alien leader of this gallaxy is furious! Something big is coming!", True, (144, 238, 144))
            WIN.blit(warning, (settings.WIN_WIDTH // 2 - warning.get_width() // 2, 50))

        if wave_count > 20 and wave_count < 23 and boss2500 and boss2500.hp <= 1 and not boss2500.alive and boss2500_defeated: 
            font = pygame.font.SysFont("comicsans", 20)
            warning = font.render("You have official defended our world from the first evil galactic fleet. You have finishd 1 of 5 fleets", True, (144, 238, 144))
            WIN.blit(warning, (settings.WIN_WIDTH // 2 - warning.get_width() // 2, 50))

        if wave_count >= 10 and wave_count <= 12 and boss1000 and not boss1000.alive and not checkpoint_spawned:
            checkpoint = Checkpoint(x=settings.WIN_WIDTH//2 - 32, y=settings.WIN_HEIGHT//2, wave_number=22)
            checkpoint_spawned = True
            checkpoint_activated_time = None
            
        if wave_count >= 20 and wave_count <= 22 and boss2500 and not boss2500.alive and not checkpoint_spawned:
            checkpoint = Checkpoint(x=settings.WIN_WIDTH//2 - 32, y=settings.WIN_HEIGHT//2, wave_number=22)
            checkpoint_spawned = True
            checkpoint_activated_time = None


        # Draw and activate checkpoint if needed
        if checkpoint:
            if not checkpoint.activated:
                checkpoint.draw(WIN)
                checkpoint.activate(player)
                if checkpoint.activated:
                    checkpoint_activated_time = time.time()
                    player.checkpoint_wave = checkpoint.wave_number  # <--- THIS LINE IS GOLD

            else:
                # If activated, keep drawing for 2 seconds
                if checkpoint_activated_time and (time.time() - checkpoint_activated_time < 2):
                    checkpoint.draw(WIN)



        # Draw wave counter at top left
        font = pygame.font.SysFont("comicsans", 30)
        wave_text = font.render(f"Wave: {wave_count}", True, (255, 255, 255))
        WIN.blit(wave_text, (10, 10))

        pygame.display.update()
        if player.hp <= 0:
            if hasattr(player, 'checkpoint_wave') and checkpoint and checkpoint.activated:
                wave_count = player.checkpoint_wave

                enemies.clear()
                lasers.clear()
                super_lasers.clear()
                meteors.clear()

                # 🚫 Reset all bosses if checkpoint passed their wave
                boss500 = None if wave_count >= 11 else boss500
                boss1000 = None if wave_count >= 11 else boss1000
                knight = None if wave_count >= 21 else knight
                boss2500 = None if wave_count >= 21 else boss2500

                # 👾 Recreate player
                player = Defender(500, 750)

                game_over = False  # ✨ Let the game continue

            else:
                wave_count = 1  # No checkpoint? Back to start
                game_over = True


def game_loop():
    while True:
        main(WIN)

if __name__ == "__main__":
    game_loop()