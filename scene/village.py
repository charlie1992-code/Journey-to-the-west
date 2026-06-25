# scene/village.py
import pygame
from pygame.constants import QUIT

class VillageScene:
    def __init__(self, screen, map_surface, sprites=None, collision_rects=None):
        self.screen = screen
        self.map_surface = map_surface
        self.sprites = sprites if sprites else []
        self.collision_rects = collision_rects if collision_rects else []
        for sprite in self.sprites:
            if hasattr(sprite, 'set_collision_rects'):
                sprite.set_collision_rects(self.collision_rects)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # 更新所有精灵
            for sprite in self.sprites:
                sprite.update()

            # 绘制地图
            self.screen.blit(self.map_surface, (0, 0))
            # 绘制精灵
            for sprite in self.sprites:
                self.screen.blit(sprite.image, sprite.rect)

            pygame.display.update()
            clock.tick(40)
        return running