import pygame
import random
from .dir_action import DirAction

class EarthGod(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 土地公有4个方向，每个方向10帧，帧索引3位
        self.action = DirAction(
            path_name1='img',
            path_name2='god',
            prefix='0214-16505471-',
            dir_count=4,
            frame_count=10,
            is_loop=True,
            filename_template="{prefix}{d:02d}{f:03d}.tga"   # 修正：帧索引3位
        )
        self.image = self.action.get_current_image()
        self.pos_x = 0
        self.pos_y = 0
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

        self.dir = 0          # 0下, 1左, 2上, 3右
        self.step_count = 0
        self.step_limit = 10
        self.speed = 1

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.rect.topleft = (x, y)

    def update(self):
        # 移动
        if self.dir == 0:
            self.pos_y += self.speed
        elif self.dir == 1:
            self.pos_x -= self.speed
        elif self.dir == 2:
            self.pos_y -= self.speed
        elif self.dir == 3:
            self.pos_x += self.speed

        # 随机换方向
        self.step_count += 1
        if self.step_count >= self.step_limit:
            self.step_count = 0
            self.dir = random.randint(0, 3)

        # 根据方向更新动画
        self.action.set_direction(self.dir)
        self.action.update()
        self.image = self.action.get_current_image()

        self.rect.topleft = (self.pos_x, self.pos_y)

    def draw(self, surface, win_posx, win_posy):
        screen_x = self.pos_x - win_posx
        screen_y = self.pos_y - win_posy
        surface.blit(self.image, (screen_x, screen_y))