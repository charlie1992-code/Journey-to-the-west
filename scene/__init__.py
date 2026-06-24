#放置场景公用的方法类
import pygame
from utils.tiled_render import TiledRenderer

class TiledScene:
    """通用 Tiled 场景类"""

    def __init__(self, path: str):
        """
        加载并渲染地图
        :param path: .tmx 文件路径
        """
        self.tiled_path = path
        self.tiled = TiledRenderer(self.tiled_path)
        # 创建与地图等大的 Surface 并渲染
        self.surface = pygame.Surface(self.tiled.pixel_size)
        self.tiled.render_map(self.surface)