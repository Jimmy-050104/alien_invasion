import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    def __init__(self, ai_setting, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting

        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.life = 20 + 20 * ai_setting.level

        # 初始化字体设置
        self.font = pygame.font.SysFont(None, 24)
        self.text_color = (255, 255, 255)  # 白色文字

    def update(self):
        self.x += self.ai_setting.alien_speed_factor * self.ai_setting.fleet_direction
        self.rect.x = self.x
        self.y += self.ai_setting.fleet_drop_speed
        self.rect.y = int(self.y)

    def check_edge(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        return False

    def draw_health(self, screen):
        """在Alien下方绘制血量"""
        health_str = str(self.life)
        text_surface = self.font.render(health_str, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = self.rect.midbottom
        text_rect.y += 2  # 向下偏移2像素
        screen.blit(text_surface, text_rect)