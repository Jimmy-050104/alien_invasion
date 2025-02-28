class Setting():
    def __init__(self):
        self.level = 0
        # 屏幕的设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # 飞船的设置
        self.ship_sped_factor = 0.3
        self.ship_limit = 3

        # 子弹的设置
        self.bullet_speed_factor = 0.7
        self.bullet_speed_width = 3
        self.bullet_speed_height = 5
        self.bullet_speed_color = 60,60,60
        self.bullet_cooldown = 300
        self.bullet_power = 30

        #外星人设置
        self.alien_speed_factor = 0.08
        self.fleet_drop_speed = 0.01
        self.fleet_direction = 1
        self.speedup_scale = 1.1
        self.alien_life = 20+20*self.level

        self.alien_points = 50

    def increase_speed(self):
        self.alien_speed_factor *= self.speedup_scale

    def reset(self):
        self.alien_speed_factor = 0.08
        self.bullet_power = 30
        self.bullet_speed_width = 3

