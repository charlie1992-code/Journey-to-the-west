# actor/cattle_battle.py
import enum
import pygame
from .dir_action import DirAction

class CattleBattleStatus(enum.IntEnum):
    """怪物打斗状态枚举"""
    Station = 0      # 站立
    Fight = 1        # 攻击
    Die = 2          # 死亡中
    DieOver = 3      # 死亡结束

class CattleBattle(pygame.sprite.Sprite):
    """
    打斗中的怪物（牛怪）
    整合了不同状态的动画切换与逻辑
    """
    def __init__(self, pos_x: int = 0, pos_y: int = 0, hp: int = 20):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.hp = hp
        self.status = CattleBattleStatus.Station

        # ---------- 加载各状态动画 ----------
        # 死亡动画（resource/img/cattle/die/）
        self.die = DirAction(
            path_name1='img',
            path_name2='cattle/die',
            prefix='0762-4cbbea5a-',
            dir_count=4,
            frame_count=11,
            is_loop=False,
            filename_template="{prefix}{d:02d}{f:03d}.tga"
        )

        # 攻击动画（resource/img/cattle/fight/）
        self.fight = DirAction(
            path_name1='img',
            path_name2='cattle/fight',
            prefix='0618-3c4fe166-',
            dir_count=4,
            frame_count=13,
            is_loop=False,
            filename_template="{prefix}{d:02d}{f:03d}.tga"
        )

        # 站立动画（resource/img/cattle/station/）
        self.station = DirAction(
            path_name1='img',
            path_name2='cattle/station',
            prefix='1644-a85e8726-',
            dir_count=4,
            frame_count=2,
            is_loop=True,
            filename_template="{prefix}{d:02d}{f:03d}.tga"
        )

        self.image = self.station.get_current_image()
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def set_pos(self, x, y):
        """设置位置"""
        self.pos_x = x
        self.pos_y = y
        self.rect.topleft = (int(x), int(y))

    def set_status(self, status: CattleBattleStatus):
        """切换战斗状态并重置相关动画"""
        self.status = status
        if status == CattleBattleStatus.Station:
            self.station.reset()
        elif status == CattleBattleStatus.Fight:
            self.fight.reset()
        elif status == CattleBattleStatus.Die:
            self.die.reset()

    def attack_hp(self, damage: int):
        """受到伤害，减少血量"""
        self.hp -= damage
        if self.hp <= 0:
            self.set_status(CattleBattleStatus.Die)

    def action_over(self) -> bool:
        """判断当前动作是否播放完毕"""
        if self.status == CattleBattleStatus.Fight:
            return self.fight.is_end()
        elif self.status == CattleBattleStatus.Die:
            if self.die.is_end():
                self.set_status(CattleBattleStatus.DieOver)
            return self.die.is_end()
        elif self.status == CattleBattleStatus.Station:
            return self.station.is_end()
        return False

    def update(self):
        """每帧更新动画"""
        if self.status == CattleBattleStatus.Station:
            self.station.update()
            self.image = self.station.get_current_image()
        elif self.status == CattleBattleStatus.Fight:
            self.fight.update()
            self.image = self.fight.get_current_image()
            if self.fight.is_end():
                # 攻击结束回到站立
                self.set_status(CattleBattleStatus.Station)
        elif self.status == CattleBattleStatus.Die:
            self.die.update()
            self.image = self.die.get_current_image()
            if self.die.is_end():
                self.set_status(CattleBattleStatus.DieOver)
        elif self.status == CattleBattleStatus.DieOver:
            # 保持最后一帧
            pass

        self.rect.topleft = (int(self.pos_x), int(self.pos_y))

    def draw(self, surface: pygame.Surface, win_pos_x: int = 0, win_pos_y: int = 0):
        """绘制到目标表面，考虑视口偏移"""
        screen_x = int(self.pos_x - win_pos_x)
        screen_y = int(self.pos_y - win_pos_y)

        # 根据状态获取当前帧
        dir = 2  # 默认方向（正对玩家）
        if self.status == CattleBattleStatus.Station:
            image = self.station.get_current_image()
        elif self.status == CattleBattleStatus.Fight:
            image = self.fight.get_current_image()
        elif self.status == CattleBattleStatus.Die:
            image = self.die.get_current_image()
        elif self.status == CattleBattleStatus.DieOver:
            image = self.die.get_current_image()
        else:
            image = self.station.get_current_image()

        surface.blit(image, (screen_x, screen_y))

        # 绘制血条（可选）
        if self.hp > 0:
            bar_width = 40
            bar_height = 5
            bar_x = screen_x + 10
            bar_y = screen_y - 10
            # 背景（灰色）
            pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
            # 血量（绿色）
            hp_width = int(bar_width * (self.hp / 20))  # 假设满血20
            if hp_width > 0:
                pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, hp_width, bar_height))