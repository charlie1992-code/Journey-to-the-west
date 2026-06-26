# actor/cattle.py
import pygame
import random
from .dir_action import DirAction

class Cattle(pygame.sprite.Sprite):
    def __init__(self, init_pos_x: int, init_pos_y: int):
        super().__init__()
        self.pos_x = init_pos_x
        self.pos_y = init_pos_y

        # 路径：resource/img/cattle/walk1/
        self.walk_frames = DirAction(
            path_name1='img',
            path_name2='cattle/walk1',
            prefix='1252-7f2abf21-',
            dir_count=4,
            frame_count=8,
            is_loop=True,
            filename_template="{prefix}{d:02d}{f:03d}.tga"
        )
        self.image = self.walk_frames.get_current_image()
        self.width = 124
        self.height = 186
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

        self.step_count = 0
        self.dir = 2
        self.speed = 0.05         # 速度从3改为1，更慢
        self.is_stop = False

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.rect.topleft = (x, y)

    def draw(self, surface: pygame.Surface, win_pos_x, win_pos_y):
        self.walk_frames.set_direction(self.dir)
        self.walk_frames.update()
        self.image = self.walk_frames.get_current_image()
        screen_x = self.pos_x - win_pos_x
        screen_y = self.pos_y - win_pos_y
        surface.blit(self.image, (screen_x, screen_y))

    def Move(self):
        if not self.is_stop:
            self.step_count += 1
            if self.step_count >= 10:
                self.step_count = 0
                self.dir = random.randint(0, 3)

            if self.dir == 0:
                self.pos_y += self.speed
            elif self.dir == 1:
                self.pos_x -= self.speed
            elif self.dir == 2:
                self.pos_y -= self.speed
            elif self.dir == 3:
                self.pos_x += self.speed

            self.rect.topleft = (self.pos_x, self.pos_y)

    def collide(self, sprite):
        if pygame.sprite.collide_rect(sprite, self):
            self.is_stop = True
            return True
        else:
            self.is_stop = False
            return False