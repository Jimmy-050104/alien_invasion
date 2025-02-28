import random
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

####

def check_events(ai_setting, screen, aliens, ship, bullets, last_bullet_time, play_button, stats, sb, bullet_sound):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            last_bullet_time = check_keydown_events(event, ai_setting, screen, ship, bullets, last_bullet_time, bullet_sound)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, aliens, ship, bullets, play_button, stats, mouse_x, mouse_y, sb)
    return last_bullet_time

def check_play_button(ai_setting,screen,aliens,ship,bullets,play_button,stats,mouse_x,mouse_y,sb):
    if play_button.rect.collidepoint(mouse_x,mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
        if button_clicked and not stats.game_active:
            stats.reset_stats()
            stats.game_active = True

            aliens.empty()
            bullets.empty()

            create_fleet(ai_setting,screen,ship,aliens,sb)
            ship.center_ship()

            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()


def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_forward = False
    elif event.key == pygame.K_DOWN:
        ship.moving_back = False


def check_keydown_events(event, ai_setting, screen, ship, bullets, last_bullet_time, bullet_sound):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_forward = True
    elif event.key == pygame.K_DOWN:
        ship.moving_back = True
    elif event.key == pygame.K_SPACE:
        last_bullet_time = fire_bullet(ai_setting, bullets, screen, ship, last_bullet_time, bullet_sound)
    return last_bullet_time

####



def fire_bullet(ai_setting, bullets, screen, ship, last_bullet_time, bullet_sound):
    current_time = pygame.time.get_ticks()
    if current_time - last_bullet_time > ai_setting.bullet_cooldown:
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)
        # bullet_sound.play()  # 播放子弹发射音效
        last_bullet_time = current_time
    return last_bullet_time



def update_screen(ai_setting,screen,ship,aliens,bullets,play_button,stats,sb):
    screen.fill(ai_setting.bg_color)
    for bullet in bullets:
        bullet.drew_bullet()
    ship.blitme()
    aliens.draw(screen)
    for alien in aliens.sprites():
        alien.draw_health(screen)
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def update_bullets(ai_setting, aliens, bullets, screen, ship, sb, stats, explosion_sound):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_setting, aliens, bullets, screen, ship, sb, stats, explosion_sound)


def check_bullet_alien_collisions(ai_setting, aliens, bullets, screen, ship, sb, stats,explosion_sound):
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, False)

    if collisions:
        for bullet, collided_aliens in collisions.items():
            for alien in collided_aliens:
                alien.life -= bullet.power
                if alien.life <= 0:
                    # explosion_sound.play()
                    aliens.remove(alien)
                    bullets.remove(bullet)
                    stats.score += ai_setting.alien_points
                    sb.prep_score()
                    check_high_score(stats, sb)
                else:
                    bullets.remove(bullet)
                    break
        if len(aliens) == 0:
            r = random.randint(0,2)
            if r == 0:
                ai_setting.bullet_power += 30
                sb.prep_power()
            elif r == 1:
                ai_setting.bullet_speed_width += 30
            bullets.empty()
            create_fleet(ai_setting, screen, ship, aliens, sb)
            ai_setting.increase_speed()


def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


####创建外星人

def create_fleet(ai_setting,screen,ship,aliens,sb):
    alien = Alien(ai_setting,screen)
    alien_width = alien.rect.width
    number_row = get_number_row(ai_setting,ship.rect.height,alien.rect.height)

    for row_number in range(number_row):
        for alien_number in range(get_number_aliens_x(ai_setting, alien_width)):
            create_alien(ai_setting, alien_number, aliens, screen,row_number)
    ai_setting.level += 1
    sb.prep_level()



def create_alien(ai_setting, alien_number, aliens, screen,row_number):
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien.rect.height + 2 * alien.rect.height*row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)


def get_number_aliens_x(ai_setting, alien_width):
    available_aliens_x = ai_setting.screen_width - 2 * alien_width
    max_number_aliens_x = int(available_aliens_x / (2 * alien_width))
    number_aliens_x = ai_setting.level//3 + random.randint(1,ai_setting.level+1)
    if number_aliens_x >= max_number_aliens_x:
        number_aliens_x = max_number_aliens_x
    return number_aliens_x

def get_number_row(ai_setting,ship_height,alien_height):
    available_space_y = (ai_setting.screen_height - (3*alien_height) - ship_height)
    max_number_rows = int(available_space_y/(2*alien_height))
    if ai_setting.level//2 < max_number_rows:
        number_rows = ai_setting.level//2 + 1
    else:
        number_rows = max_number_rows
    return number_rows

####

def update_aliens(ai_setting,stats,screen,ship,aliens,bullets,sb):
    check_fleet_edges(ai_setting,aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_setting,stats,screen,ship,aliens,bullets,sb)

    check_aliens_bottom(ai_setting,stats,screen,ship,aliens,bullets,sb)


def ship_hit(ai_setting,stats,screen,ship,aliens,bullets,sb):
        if stats.ships_left > 0:
            stats.ships_left -= 1

            sb.prep_ships()

            aliens.empty()
            bullets.empty()

            ai_setting.level = 0
            ai_setting.reset()
            sb.prep_level()
            create_fleet(ai_setting,screen,ship,aliens,sb)
            ship.center_ship()

            sleep(0.5)
        else:
            stats.game_active = False

def check_aliens_bottom(ai_setting,stats,screen,ship,aliens,bullets,sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting,stats,screen,ship,aliens,bullets,sb)
            break


def check_fleet_edges(ai_setting,aliens):
    for alien in aliens.sprites():
        if alien.check_edge():
            ai_setting.fleet_direction *= -1
            break

dict()