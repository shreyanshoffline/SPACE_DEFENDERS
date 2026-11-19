import pygame
def handle_enemy_defender_collisions(player, enemies, game_over=None):
    for enemy in enemies:
        if enemy.alive:
            enemy_rect = enemy.img.get_rect(topleft=(enemy.x, enemy.y))
            defender_rect = player.img.get_rect(topleft=(player.x, player.y))

            if enemy_rect.colliderect(defender_rect):
                player.take_damage(5)
                enemy.alive = False

def handle_boss_defender_collisions(player, bosses, game_over=None):
    for boss in bosses:
        if boss and boss.alive:
            boss_rect = boss.get_rect()
            defender_rect = player.img.get_rect(topleft=(player.x, player.y))
            if boss_rect.colliderect(defender_rect):
                player.take_damage(250)
                boss.alive = False


def handle_laser_enemy_collisions(lasers, super_lasers, enemies, super_ready, enemy_kills, total_damage_dealt):
    hit_lasers = []
    for laser in lasers + super_lasers:
        for enemy in enemies:
            if not enemy.alive or laser.remaining_damage <= 0:
                continue
            if laser.img.get_rect(topleft=(laser.x, laser.y)).colliderect(enemy.img.get_rect(topleft=(enemy.x, enemy.y))):
                if hasattr(laser, 'frozen') and laser.frozen:
                    enemy.hit(enemy.health)
                    enemy_kills += 1
                    total_damage_dealt += laser.damage
                    break
                else:
                    damage_to_deal = min(laser.remaining_damage, enemy.health)
                    enemy.hit(damage_to_deal)
                    laser.remaining_damage -= damage_to_deal
                    if not laser.super_laser:
                        hit_lasers.append(laser)
                    elif laser.super_laser and laser.remaining_damage <= 0:
                        hit_lasers.append(laser)
                    if not enemy.alive:
                        enemy_kills += 1
                        total_damage_dealt += laser.damage
                    break
    if enemy_kills > 0 and enemy_kills % 10 == 0:
        super_ready = True
    return hit_lasers, super_ready, enemy_kills, total_damage_dealt


def handle_laser_boss_collisions(lasers, super_lasers, bosses):
    hit_lasers = []
    alive_states = []
    for boss in bosses:
        if not boss or not boss.alive:
            alive_states.append(False)
            continue
        for laser in lasers + super_lasers:
            if laser.remaining_damage <= 0:
                continue
            if laser.img.get_rect(topleft=(laser.x, laser.y)).colliderect(boss.get_rect()):
                damage_to_deal = min(laser.remaining_damage, boss.hp)
                boss.hit(damage_to_deal)
                laser.remaining_damage -= damage_to_deal
                if not laser.super_laser:
                    hit_lasers.append(laser)
                elif laser.super_laser and laser.remaining_damage <= 0:
                    hit_lasers.append(laser)
                if boss.hp <= 500 and hasattr(boss, 'enraged') and not boss.enraged:
                    boss.enraged = True
                if boss.hp <= 1 and boss.alive:
                    boss.hp = 0
                    boss.alive = False
                break
        alive_states.append(boss.alive)
    return hit_lasers, alive_states

def handle_boss_attacks_defender_collisions(player, attacks, game_over=None):
    for attack in attacks:
        attack_rect = attack.img.get_rect(topleft=(attack.x, attack.y))
        player_rect = player.img.get_rect(topleft=(player.x, player.y))
        if attack_rect.colliderect(player_rect):
            player.hp -= attack.damage  # Assuming attacks have a damage attribute
            attacks.remove(attack)
            if player.hp <= 0:
                game_over = True
    return game_over
