import os
import pygame
from pygame.constants import QUIT
from scene import TiledScene
from actor import SWK, EarthGod
import pytmx

def main():
    pygame.init()
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption("西游记 - 碰撞检测")

    tmx_path = os.path.join("resource", "tmx", "village.tmx")
    tiled_scene = TiledScene(tmx_path)
    full_map = tiled_scene.surface
    map_width, map_height = full_map.get_size()

    # 障碍物组
    obstacle_group = pygame.sprite.Group()

    spawn_swk = (100, 100)
    spawn_god = (200, 200)

    for group in tiled_scene.tiled.tmx_data.objectgroups:
        if isinstance(group, pytmx.TiledObjectGroup):
            if group.name == 'actor':
                for obj in group:
                    if obj.name == 'sun':
                        spawn_swk = (int(obj.x), int(obj.y))
                        print(f"孙悟空位置: {spawn_swk}")
            elif group.name == 'god':
                for obj in group:
                    if obj.name == 'god':
                        spawn_god = (int(obj.x), int(obj.y))
                        print(f"土地公位置: {spawn_god}")
            elif group.name == 'obstacle':   # 必须与 Tiled 层名一致
                for obj in group:
                    obs = pygame.sprite.Sprite()
                    obs.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    obstacle_group.add(obs)
                    print(f"障碍物: ({obj.x}, {obj.y}, {obj.width}, {obj.height})")

    swk = SWK()
    earth_god = EarthGod()
    swk.set_pos(*spawn_swk)
    earth_god.set_pos(*spawn_god)
    swk.set_obstacles(obstacle_group)

    # 视口初始化
    view_x = max(0, min(spawn_swk[0] - WINDOW_WIDTH//2, map_width - WINDOW_WIDTH))
    view_y = max(0, min(spawn_swk[1] - WINDOW_HEIGHT//2, map_height - WINDOW_HEIGHT))
    if map_width <= WINDOW_WIDTH:
        view_x = 0
    if map_height <= WINDOW_HEIGHT:
        view_y = 0

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        swk.update()
        earth_god.update()

        # 视口跟随
        px, py = swk.pos_x, swk.pos_y
        target_x = px - WINDOW_WIDTH//2
        target_y = py - WINDOW_HEIGHT//2
        target_x = max(0, min(target_x, map_width - WINDOW_WIDTH))
        target_y = max(0, min(target_y, map_height - WINDOW_HEIGHT))
        if map_width <= WINDOW_WIDTH:
            target_x = 0
        if map_height <= WINDOW_HEIGHT:
            target_y = 0
        view_x, view_y = target_x, target_y

        view_surface = full_map.subsurface((view_x, view_y, WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(view_surface, (0, 0))
        swk.draw(screen, view_x, view_y)
        earth_god.draw(screen, view_x, view_y)

        pygame.display.update()
        clock.tick(40)

if __name__ == "__main__":
    main()