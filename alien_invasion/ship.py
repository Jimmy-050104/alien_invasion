# import pygame
# from pygame.sprite import Sprite
#
# class Ship(Sprite):
#     def __init__(self,screen,ai_setting):
#         super(Ship,self).__init__()
#         self.screen = screen
#
#         self.image = pygame.image.load("images/ship.bmp")
#         self.rect = self.image.get_rect()
#         self.screen_rect = screen.get_rect()
#         self.ai_setting = ai_setting
#
#         self.rect.centerx = self.screen_rect.centerx
#         self.rect.bottom = self.screen_rect.bottom
#
#         self.center = float(self.rect.centerx)
#         self.bottom = float(self.rect.bottom)
#
#
#         self.moving_right = False
#         self.moving_left = False
#         self.moving_forward = False
#         self.moving_back = False
#
#         self.font = pygame.font.SysFont(None, 24)
#         self.text_color = (0, 0, 0)
#
#     def blitme(self):
#         self.screen.blit(self.image,self.rect)
#
#     def update(self):
#         if self.moving_right and self.rect.right < self.screen_rect.right:
#             self.center += self.ai_setting.ship_sped_factor
#         elif self.moving_left and self.rect.left > 0:
#             self.center -= self.ai_setting.ship_sped_factor
#         elif self.moving_forward and self.rect.top > 0:
#             self.bottom -= self.ai_setting.ship_sped_factor
#         elif self.moving_back and self.rect.bottom < self.screen_rect.bottom:
#             self.bottom += self.ai_setting.ship_sped_factor
#
#         self.rect.centerx = self.center
#         self.rect.bottom = self.bottom
#
#     def center_ship(self):
#         self.center = self.screen_rect.centerx
#         self.bottom = self.screen_rect.bottom
#
#     def draw_buff(self,buff,screen):
#         buff_str = str(buff)
#         text_surface = self.font.render(buff_str, True, self.text_color)
#         text_rect = text_surface.get_rect()
#         text_rect.midtop = self.rect.midbottom
#         text_rect.y += 2  # 向下偏移2像素
#         screen.blit(text_surface, text_rect)
#
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, screen, ai_setting):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting

        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        self.moving_right = False
        self.moving_left = False
        self.moving_forward = False
        self.moving_back = False

        # Buff 相关变量
        self.buff_message = None
        self.buff_start_time = 0
        self.font = pygame.font.SysFont("SimHei", 16)  # 设置字体

    def blitme(self):
        """绘制飞船"""
        self.screen.blit(self.image, self.rect)

        # 处理 buff 显示
        if self.buff_message:
            current_time = pygame.time.get_ticks()
            if current_time - self.buff_start_time < 1000:  # 1秒显示
                buff_text = self.font.render(self.buff_message, True, (0, 0, 0))
                self.screen.blit(buff_text, (self.rect.centerx - 50, self.rect.top - 30))
            else:
                self.buff_message = None  # 1秒后清除 buff 显示

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_setting.ship_sped_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_setting.ship_sped_factor
        elif self.moving_forward and self.rect.top > 0:
            self.bottom -= self.ai_setting.ship_sped_factor
        elif self.moving_back and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_setting.ship_sped_factor

        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def center_ship(self):
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom

    def apply_buff(self, buff_type,sb):
        """应用 buff 并显示信息"""
        if buff_type == 0:
            self.ai_setting.bullet_power += 30
            self.buff_message = "子弹威力增加!"
            sb.prep_power()
        elif buff_type == 1:
            self.ai_setting.bullet_speed_width += 30
            self.buff_message = "子弹宽度增加!"
        elif buff_type == 2:
            self.buff_message = "未获得buff"

        self.buff_start_time = pygame.time.get_ticks()  # 记录 buff 开始时间
