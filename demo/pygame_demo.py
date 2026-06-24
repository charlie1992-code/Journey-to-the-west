import pygame
import sys
import os
from pytmx import *
from pytmx.util_pygame import load_pygame

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 向上退一级目录 (到 Pygame 文件夹)，再进入 resource 文件夹找 map1.tmx
map_path = os.path.join(current_dir, "", "resource", "map1.tmx")


class TiledRenderer(object):
    def __init__(self, filename):
        # 检查文件是否存在，如果不存在会打印错误并退出，防止报错
        if not os.path.exists(filename):
            print(f"❌ 错误：找不到地图文件！\n路径：{filename}")
            sys.exit()

        tm = load_pygame(filename)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm

    def render_map(self, surface):
        if self.tmx_data.background_color:
            surface.fill(pygame.Color(self.tmx_data.background_color))

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                self.render_tile_layer(surface, layer)
            elif isinstance(layer, TiledObjectGroup):
                self.render_object_layer(surface, layer)
            elif isinstance(layer, TiledImageLayer):
                self.render_image_layer(surface, layer)

    def render_tile_layer(self, surface, layer):
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        surface_blit = surface.blit
        for x, y, image in layer.tiles():
            if image:
                surface_blit(image, (x * tw, y * th))

    def render_object_layer(self, surface, layer):
        draw_rect = pygame.draw.rect
        draw_lines = pygame.draw.lines
        surface_blit = surface.blit
        rect_color = (255, 0, 0)
        poly_color = (0, 255, 0)
        for obj in layer:
            if hasattr(obj, 'points'):
                draw_lines(surface, poly_color, obj.closed, obj.points, 3)
            elif obj.image:
                surface_blit(obj.image, (obj.x, obj.y))
            else:
                draw_rect(surface, rect_color, (obj.x, obj.y, obj.width, obj.height), 3)

    def render_image_layer(self, surface, layer):
        if layer.image:
            surface.blit(layer.image, (0, 0))


# 程序入口
if __name__ == "__main__":
    pygame.init()

    # 关键修复：先创建一个临时窗口，让 Pygame 拥有合法的显示格式
    # 这样后续加载地图时调用 convert() 就不会出错
    pygame.display.set_mode((1, 1))

    # 打印一下路径，方便你检查对错
    print(f"正在尝试加载地图，路径为：{map_path}")

    # 使用拼接好的绝对路径加载地图（此时窗口已存在，convert() 正常）
    tile_render = TiledRenderer(map_path)

    # 获取地图实际尺寸并重新设置窗口
    screen = pygame.display.set_mode(tile_render.size)
    pygame.display.set_caption("地图测试")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        tile_render.render_map(screen)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()