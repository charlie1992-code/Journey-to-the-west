import pygame
import os
from scene import TiledScene
from scene.village import VillageScene

def main():
    pygame.init()

    # ① 设定固定窗口大小（根据您截图里的显示，这里用 800x600，您可按需调整）
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Village Scene")

    # ② 加载原始地图（此时 display 已存在，不会报错）
    tiled_path = os.path.join("resource", "tmx", "village.tmx")
    tiled_scene = TiledScene(tiled_path)
    raw_map_surface = tiled_scene.surface   # 原始尺寸的地图

    # ③ 将地图缩放到窗口大小（直接拉伸填满）
    scaled_map = pygame.transform.scale(raw_map_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    # 若希望保持宽高比并居中，可改用下方注释掉的代码（见后）

    # ④ 传入缩放后的地图表面，场景直接显示
    village = VillageScene(screen, scaled_map)
    village.run()

    pygame.quit()

if __name__ == "__main__":
    main()