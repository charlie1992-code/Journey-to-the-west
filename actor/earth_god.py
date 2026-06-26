import pygame
import random
from .dir_action import DirAction

class EarthGod(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 土地公有4个方向，每方向10帧
        self.action = DirAction(
            path_name1='img',
            path_name2='god',
            prefix='0214-16505471-',
            dir_count=4,
            frame_count=10,
            is_loop=True,
            filename_template="{prefix}{d:02d}{f:03d}.tga"
        )
        self.image = self.action.get_current_image()
        self.pos_x = 0
        self.pos_y = 0
        # 土地公的碰撞盒使用整个图片大小（或可根据需要调整）
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

        self.dir = 0          # 0下, 1左, 2上, 3右
        self.step_count = 0
        self.step_limit = 10
        self.speed = 1
        self.is_stop = False  # 是否被撞停

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.rect.topleft = (x, y)

    def collide(self, sprite):
        """检测与另一个精灵的碰撞（使用 pygame.sprite.collide_rect）"""
        if pygame.sprite.collide_rect(sprite, self):
            self.is_stop = True
            return True
        else:
            self.is_stop = False
            return False

    def update(self):
        if self.is_stop:
            return  # 如果被撞停，不移动

        # 移动
        if self.dir == 0:
            self.pos_y += self.speed
        elif self.dir == 1:
            self.pos_x -= self.speed
        elif self.dir == 2:
            self.pos_y -= self.speed
        elif self.dir == 3:
            self.pos_x += self.speed

        self.step_count += 1
        if self.step_count >= self.step_limit:
            self.step_count = 0
            self.dir = random.randint(0, 3)

        self.action.set_direction(self.dir)
        self.action.update()
        self.image = self.action.get_current_image()
        self.rect.topleft = (self.pos_x, self.pos_y)

    def draw(self, surface, win_posx, win_posy):
        screen_x = self.pos_x - win_posx
        screen_y = self.pos_y - win_posy
        surface.blit(self.image, (screen_x, screen_y))