# scene/fade_scene.py
import pygame
from enum import IntEnum

class SceneStatus(IntEnum):
    In = 1
    Normal = 2
    Out = 3

class FadeScene:
    def __init__(self, back_image: pygame.Surface, window_size=(800, 600), fade_speed=10):
        """
        :param back_image: 背景 Surface
        :param window_size: 窗口大小
        :param fade_speed: 每帧透明度变化量（越大过渡越快），默认10，约2.5秒完成
        """
        self.back_image = back_image
        self.window_size = window_size
        self.fade_speed = fade_speed
        self.alpha = 0
        self.status = SceneStatus.In

    def set_status(self, status: SceneStatus):
        self.status = status
        if status == SceneStatus.In:
            self.alpha = 0
        elif status == SceneStatus.Normal:
            self.alpha = 255
        elif status == SceneStatus.Out:
            self.alpha = 0

    def is_out_complete(self) -> bool:
        return self.status == SceneStatus.Out and self.alpha >= 255

    def get_back_image(self, x: int, y: int) -> pygame.Surface:
        map_w, map_h = self.back_image.get_size()
        x = max(0, min(x, map_w - self.window_size[0]))
        y = max(0, min(y, map_h - self.window_size[1]))

        temp_surface = self.back_image.subsurface(
            (x, y, self.window_size[0], self.window_size[1])
        )

        if self.status == SceneStatus.Normal:
            return temp_surface

        elif self.status == SceneStatus.In:
            temp_surface.set_alpha(self.alpha)
            black_surface = pygame.Surface(self.window_size)
            black_surface.fill((0, 0, 0))
            black_surface.blit(temp_surface, (0, 0))
            self.alpha += self.fade_speed
            if self.alpha >= 255:
                self.alpha = 255
                self.status = SceneStatus.Normal
            return black_surface

        elif self.status == SceneStatus.Out:
            fade_alpha = 255 - self.alpha
            temp_surface.set_alpha(fade_alpha)
            black_surface = pygame.Surface(self.window_size)
            black_surface.fill((0, 0, 0))
            black_surface.blit(temp_surface, (0, 0))
            self.alpha += self.fade_speed
            if self.alpha >= 255:
                self.alpha = 255
            return black_surface