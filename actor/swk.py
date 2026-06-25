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
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

        # ===== 腰部小红点碰撞盒 =====
        # 假设图片宽58，高83（可根据实际调整）
        # 腰部大约在图片中心偏下位置，例如 (29, 55)
        self.hitbox_offset_x = 29   # 水平居中
        self.hitbox_offset_y = 55   # 垂直向下（腰部）
        self.hitbox_width = 6       # 小尺寸
        self.hitbox_height = 6
        # =============================

        self.hitbox = pygame.Rect(
            self.pos_x + self.hitbox_offset_x,
            self.pos_y + self.hitbox_offset_y,
            self.hitbox_width,
            self.hitbox_height
        )

        self.speed = 5
        self.obstacle_group = None

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.rect.topleft = (x, y)
        self._update_hitbox()

    def set_obstacles(self, group):
        self.obstacle_group = group

    def _update_hitbox(self):
        self.hitbox.x = self.pos_x + self.hitbox_offset_x
        self.hitbox.y = self.pos_y + self.hitbox_offset_y

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
            # 水平检测
            if dx != 0:
                new_x = self.pos_x + dx
                test_hitbox = self.hitbox.copy()
                test_hitbox.x = new_x + self.hitbox_offset_x
                collide = False
                for obs in self.obstacle_group:
                    if test_hitbox.colliderect(obs.rect):
                        collide = True
                        break
                if not collide:
                    self.pos_x = new_x
                    self.rect.x = self.pos_x
                    self._update_hitbox()

            # 垂直检测
            if dy != 0:
                new_y = self.pos_y + dy
                test_hitbox = self.hitbox.copy()
                test_hitbox.y = new_y + self.hitbox_offset_y
                collide = False
                for obs in self.obstacle_group:
                    if test_hitbox.colliderect(obs.rect):
                        collide = True
                        break
                if not collide:
                    self.pos_y = new_y
                    self.rect.y = self.pos_y
                    self._update_hitbox()

            # 方向与动画
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

        # 调试：绘制红色小点（碰撞盒）
        debug_rect = self.hitbox.copy()
        debug_rect.x -= win_posx
        debug_rect.y -= win_posy
        pygame.draw.rect(surface, (255, 0, 0), debug_rect, 1)  # 红色边框
        # 填充红色半透明（可选）
        # pygame.draw.rect(surface, (255, 0, 0, 128), debug_rect)