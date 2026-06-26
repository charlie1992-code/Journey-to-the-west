import pygame
from scene import VillageScene, TempleScene
from dialog import Dialog

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    pygame.display.set_caption("西游记 - 场景切换与对话")

    dialog = Dialog(screen)
    swk = None
    is_village = True

    while True:
        if is_village:
            scene = VillageScene(screen, swk, dialog)
        else:
            scene = TempleScene(screen, swk, dialog)

        swk = scene.run()   # 运行场景，返回玩家对象
        is_village = not is_village   # 切换场景类型

if __name__ == "__main__":
    main()