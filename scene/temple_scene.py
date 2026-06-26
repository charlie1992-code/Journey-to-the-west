# scene/temple_scene.py
import os
import pygame
from pygame.constants import QUIT
from . import TiledScene
from .fade_scene import FadeScene, SceneStatus
from actor.swk import SWK
from actor.cattle import Cattle
from dialog import Dialog
import pytmx

class TempleScene:
    def __init__(self, surface: pygame.Surface, swk: SWK, dialog: Dialog = None):
        self.screen = surface
        self.dialog = dialog
        self.swk_player = swk
        self.swk_player.set_pos(100, 100)

        backtmxpath = os.path.join('resource', 'tmx', 'temple.tmx')
        self.tiled_scene = TiledScene(backtmxpath)
        self.back_surface = self.tiled_scene.surface

        self.fade_scene = FadeScene(self.back_surface, fade_speed=8)
        self.temp_surface = pygame.Surface((800, 600))
        self.obstacle_group = pygame.sprite.Group()

        self.win_pos_x = 0
        self.win_pos_y = 0

        self.monsters = []

        self.init_actor()
        self.fade_scene.set_status(SceneStatus.In)

    def init_actor(self):
        for group in self.tiled_scene.tiled.tmx_data.objectgroups:
            if isinstance(group, pytmx.TiledObjectGroup):
                if group.name == 'actor':
                    for obj in group:
                        if obj.name == 'sun':
                            self.swk_player.set_pos(obj.x, obj.y)
                            self.win_pos_x = obj.x - 400
                            self.win_pos_y = obj.y - 300
                elif group.name == 'obstacle':
                    for obj in group:
                        obs = pygame.sprite.Sprite()
                        obs.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.obstacle_group.add(obs)
                elif group.name == 'monster':
                    for obj in group:
                        monster = Cattle(obj.x, obj.y)
                        self.monsters.append(monster)
        self.swk_player.set_obstacles(self.obstacle_group)

    def get_current_surface(self):
        win_surface = self.fade_scene.get_back_image(self.win_pos_x, self.win_pos_y)
        self.temp_surface.blit(win_surface, (0, 0))
        self.swk_player.draw(self.temp_surface, self.win_pos_x, self.win_pos_y)
        for monster in self.monsters:
            monster.draw(self.temp_surface, self.win_pos_x, self.win_pos_y)
        return self.temp_surface

    def run(self):
        clock = pygame.time.Clock()
        while True:
            key_down = False
            dx_dy = [0, 0]
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    key_down = True
                    pressed_key = event.key

                    if self.dialog and self.dialog.visible:
                        if pressed_key == pygame.K_y:
                            self.fade_scene.set_status(SceneStatus.Out)
                        elif pressed_key == pygame.K_n:
                            self.dialog.hide()
                            for monster in self.monsters:
                                monster.is_stop = False
                        continue

                    if pressed_key == pygame.K_t:
                        self.fade_scene.set_status(SceneStatus.Out)
                    if self.fade_scene.status == SceneStatus.Normal:
                        dx_dy = self.swk_player.key_move(pressed_key, key_down, self.obstacle_group)
                        # key_move 会立即移动位置，但视口更新放在每帧统一处理
                        # 注意：这里使用 key_move 是单次按键，如果长按，建议用 update

            # 长按移动（由 swk_player.update 处理）和视口更新（每帧）
            if self.fade_scene.status == SceneStatus.Normal and not (self.dialog and self.dialog.visible):
                # 调用 update 处理长按移动（内部根据按键状态移动）
                self.swk_player.update()

                # 更新怪物
                for monster in self.monsters:
                    monster.Move()

                # 视口跟随玩家（始终居中）
                px, py = self.swk_player.pos_x, self.swk_player.pos_y
                target_x = px - 400
                target_y = py - 300
                map_w, map_h = self.back_surface.get_size()
                self.win_pos_x = max(0, min(target_x, map_w - 800))
                self.win_pos_y = max(0, min(target_y, map_h - 600))

            # 对话框可见时暂停逻辑（但视口保持）
            if self.dialog and self.dialog.visible:
                surface = self.get_current_surface()
                self.screen.blit(surface, (0, 0))
                self.dialog.draw()
                pygame.display.update()
                clock.tick(40)
                if self.fade_scene.is_out_complete():
                    break
                continue

            surface = self.get_current_surface()
            self.screen.blit(surface, (0, 0))
            if self.dialog:
                self.dialog.draw()
            pygame.display.update()
            clock.tick(30)

            if self.fade_scene.is_out_complete():
                break

        return self.swk_player