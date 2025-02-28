import pygame
from setting import Setting
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import pygame.mixer

def run_game():
    pygame.init()
    ai_setting = Setting()
    screen = pygame.display.set_mode((ai_setting.screen_width,ai_setting.screen_height))
    pygame.display.set_caption("alien_invasion")


    # pygame.mixer.music.load('sounds/外星人入侵-Alien_Invasion_Underscor_爱给网_aigei_com.mp3')
    # pygame.mixer.music.play(-1)

    bullet_sound = pygame.mixer.Sound('sounds/外星人入侵游戏武器音效 (15)_爱给网_aigei_com.mp3')
    explosion_sound = pygame.mixer.Sound('sounds/勘探中火热爆-爆炸- 火球爆裂(Explo_Medium_F_爱给网_aigei_com.mp3')

    play_button = Button(ai_setting,screen,"Play")
    stats = GameStats(ai_setting)
    sb = Scoreboard(ai_setting,screen,stats)
    ship = Ship(screen,ai_setting)
    bullets = Group()
    aliens = Group()
    last_bullet_time = 0

    while True:
        last_bullet_time = gf.check_events(ai_setting, screen, aliens, ship, bullets, last_bullet_time, play_button,stats, sb, bullet_sound)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_setting, aliens, bullets, screen, ship, sb, stats, explosion_sound)
            gf.update_aliens(ai_setting, stats, screen, ship, aliens, bullets, sb)
        gf.update_screen(ai_setting, screen, ship, aliens, bullets, play_button, stats, sb)

if __name__ == '__main__':
    run_game()