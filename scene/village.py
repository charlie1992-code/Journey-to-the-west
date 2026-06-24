import pygame
from pygame.constants import QUIT

class VillageScene:
    def __init__(self, screen: pygame.Surface, map_surface: pygame.Surface):
        """
        :param screen: 主窗口 Surface
        :param map_surface: 已渲染好的地图 Surface
        """
        self.screen = screen
        self.map_surface = map_surface

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.screen.blit(self.map_surface, (0, 0))
            pygame.display.update()
            clock.tick(40)
        return running