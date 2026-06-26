# scene/__init__.py
import pygame
from utils.tiled_render import TiledRenderer
from pytmx import TiledTileLayer, TiledImageLayer, TiledObjectGroup

# ======================== TiledScene 类 ========================
class TiledScene:
    def __init__(self, path: str):
        self.tiled_path = path
        self.tiled = TiledRenderer(self.tiled_path)
        self.tmx_data = self.tiled.tmx_data
        self.surface = pygame.Surface(self.tiled.pixel_size)
        self._render_without_objects()
        self.collision_rects = []
        self.player_spawn = None
        self._extract_objects()

        if self.player_spawn:
            print(f"✅ 玩家位置已提取: ({self.player_spawn[0]}, {self.player_spawn[1]})")
        else:
            print("⚠️ 未找到玩家位置对象")

    def _render_without_objects(self):
        surface = self.surface
        if self.tmx_data.background_color:
            surface.fill(pygame.Color(self.tmx_data.background_color))
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                self._render_tile_layer(surface, layer)
            elif isinstance(layer, TiledImageLayer):
                self._render_image_layer(surface, layer)

    def _render_tile_layer(self, surface, layer):
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        for x, y, image in layer.tiles():
            if image:
                surface.blit(image, (x * tw, y * th))

    def _render_image_layer(self, surface, layer):
        if layer.image:
            surface.blit(layer.image, (0, 0))

    def _extract_objects(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledObjectGroup):
                for obj in layer:
                    is_player = False
                    if obj.name and obj.name.lower() in ("sun", "player"):
                        is_player = True
                    elif obj.image:
                        is_player = True
                    elif hasattr(obj, 'properties') and obj.properties.get('type') == 'player':
                        is_player = True

                    if is_player:
                        self.player_spawn = (obj.x, obj.y)
                        print(f"🎯 识别到玩家对象: 名称='{obj.name}', 坐标=({obj.x}, {obj.y})")
                        return

                    if not hasattr(obj, 'points') and not obj.image:
                        self.collision_rects.append(
                            pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        )

# ======================== 场景切换相关 ========================
from .fade_scene import FadeScene, SceneStatus
from .village import VillageScene
from .temple_scene import TempleScene

# ======================== 统一导出 ========================
__all__ = [
    'TiledScene',
    'FadeScene',
    'SceneStatus',
    'VillageScene',
    'TempleScene',
]