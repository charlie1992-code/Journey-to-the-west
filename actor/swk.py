import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from .dir_action import DirAction

class SWK(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.action = DirAction(
            path_name1='img',
            path_name2='swk',
            prefix='',
            dir_count=4,
            frame_count=4,
            is_loop=True,
            filename_template="{d:02d}{f:03d}.tga"
        )
        self.image = self.action.get_current_image()
        self.pos_x = 0
        self.pos_y = 0

        # 碰撞盒（小红点）
        self.offset_x = 34
        self.offset_y = 180
        self.collide_width = 30
        self.collide_height = 10

        self.rect = pygame.Rect(
            self.pos_x + self.offset_x,
            self.pos_y + self.offset_y,
            self.collide_width,
            self.collide_height
        )

        self.speed = 5
        self.obstacle_group = None
        self.dir = 0

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self._update_rect()

    def set_obstacles(self, group):
        self.obstacle_group = group

    def _update_rect(self):
        self.rect.x = self.pos_x + self.offset_x
        self.rect.y = self.pos_y + self.offset_y

    # ===== 新增 key_move 方法（兼容原调用） =====
    def key_move(self, pressed_key, key_click, obstacle_group=None):
        """
        单次按键移动，返回 [dx, dy]
        :param pressed_key: pygame 键码
        :param key_click: 是否按下
        :param obstacle_group: 障碍物组（可选）
        :return: [dx, dy] 移动偏移量
        """
        if not key_click:
            return [0, 0]

        dx, dy = 0, 0
        if pressed_key == K_UP:
            self.dir = 2
            dy = -10
        elif pressed_key == K_DOWN:
            self.dir = 0
            dy = 10
        elif pressed_key == K_LEFT:
            self.dir = 1
            dx = -10
        elif pressed_key == K_RIGHT:
            self.dir = 3
            dx = 10
        else:
            return [0, 0]

        # 碰撞检测（如果传入了障碍物组）
        if obstacle_group is not None:
            test_rect = self.rect.copy()
            test_rect.x += dx
            test_rect.y += dy
            for obs in obstacle_group:
                if test_rect.colliderect(obs.rect):
                    return [0, 0]   # 碰撞则不动

        self.pos_x += dx
        self.pos_y += dy
        self._update_rect()

        self.action.set_direction(self.dir)
        self.action.update()
        self.image = self.action.get_current_image()

        return [dx, dy]

    # ===== 原有 update 方法（长按移动，完全保留） =====
    def update(self):
        if self.obstacle_group is None:
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[K_UP]:
            dy = -self.speed
        if keys[K_DOWN]:
            dy = self.speed
        if keys[K_LEFT]:
            dx = -self.speed
        if keys[K_RIGHT]:
            dx = self.speed

        if dx != 0 or dy != 0:
            if dx != 0:
                new_x = self.pos_x + dx
                test_rect = self.rect.copy()
                test_rect.x = new_x + self.offset_x
                collide = False
                for obs in self.obstacle_group:
                    if test_rect.colliderect(obs.rect):
                        collide = True
                        break
                if not collide:
                    self.pos_x = new_x
                    self._update_rect()

            if dy != 0:
                new_y = self.pos_y + dy
                test_rect = self.rect.copy()
                test_rect.y = new_y + self.offset_y
                collide = False
                for obs in self.obstacle_group:
                    if test_rect.colliderect(obs.rect):
                        collide = True
                        break
                if not collide:
                    self.pos_y = new_y
                    self._update_rect()

            if dx != 0 or dy != 0:
                if dy < 0:
                    dir_index = 2
                elif dy > 0:
                    dir_index = 0
                elif dx < 0:
                    dir_index = 1
                elif dx > 0:
                    dir_index = 3
                else:
                    dir_index = self.action.current_dir

                self.action.set_direction(dir_index)
                self.action.update()
                self.image = self.action.get_current_image()

    def draw(self, surface, win_posx=0, win_posy=0):
        screen_x = self.pos_x - win_posx
        screen_y = self.pos_y - win_posy
        surface.blit(self.image, (screen_x, screen_y))

        # 调试碰撞盒（保留，您可自行注释）
        debug_rect = self.rect.copy()
        debug_rect.x -= win_posx
        debug_rect.y -= win_posy
        pygame.draw.rect(surface, (255, 0, 0), debug_rect, 1)