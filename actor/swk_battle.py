# actor/battle_swk.py
import enum
import pygame
from .dir_action import DirAction

class SwkBattleStatus(enum.IntEnum):
    """孙悟空打斗状态枚举"""
    Station = 0      # 站立
    Fight = 1        # 攻击
    Escape = 2       # 逃跑中
    EscapeOver = 3   # 逃跑结束
    Die = 4          # 死亡中
    DieOver = 5      # 死亡结束

class BattleSwk(pygame.sprite.Sprite):
    """
    打斗中的孙悟空
    整合了不同状态的动画切换与逻辑
    """
    def __init__(self, hp: int, pos_x: int = 0, pos_y: int = 0):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.hp = hp
        self.status = SwkBattleStatus.Station

        # ---------- 加载各状态动画 ----------
        # 站立动画（假设资源位于 resource/img/swk/station/）
        self.station = DirAction(
            path_name1='img',
            path_name2='swk/station',
            prefix='',
            dir_count=4,
            frame_count=4,
            is_loop=True,
            filename_template="{d:02d}{f:03d}.tga"
        )

        # 攻击动画（假设资源位于 resource/img/swk/fight/）
        self.magic_fight = DirAction(
            path_name1='img',
            path_name2='swk/fight',
            prefix='',
            dir_count=4,
            frame_count=6,
            is_loop=False,          # 攻击动画不循环，播放一次结束
            filename_template="{d:02d}{f:03d}.tga"
        )

        # 死亡/逃跑动画（共用资源，假设位于 resource/img/swk/die_escape/）
        self.magic_die_escape = DirAction(
            path_name1='img',
            path_name2='swk/die_escape',
            prefix='',
            dir_count=1,            # 只取方向0（正面对玩家）
            frame_count=8,
            is_loop=False,
            filename_template="{f:03d}.tga"
        )

        self.image = self.station.get_current_image()
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def set_status(self, status: SwkBattleStatus):
        """切换战斗状态并重置相关动画"""
        self.status = status
        if status == SwkBattleStatus.Station:
            self.station.reset()
        elif status == SwkBattleStatus.Fight:
            self.magic_fight.reset()
        elif status == SwkBattleStatus.Escape:
            self.magic_die_escape.reset()
        elif status == SwkBattleStatus.Die:
            self.magic_die_escape.reset()

    def update(self):
        """每帧更新逻辑（动画推进、状态切换）"""
        if self.status == SwkBattleStatus.Station:
            self.station.update()
            self.image = self.station.get_current_image()

        elif self.status == SwkBattleStatus.Fight:
            self.magic_fight.update()
            self.image = self.magic_fight.get_current_image()
            if self.magic_fight.is_end():
                # 攻击结束回到站立
                self.set_status(SwkBattleStatus.Station)

        elif self.status == SwkBattleStatus.Die:
            self.magic_die_escape.update()
            self.image = self.magic_die_escape.get_current_image()
            if self.magic_die_escape.is_end():
                self.set_status(SwkBattleStatus.DieOver)

        elif self.status == SwkBattleStatus.Escape:
            self.magic_die_escape.update()
            self.image = self.magic_die_escape.get_current_image()
            if self.magic_die_escape.is_end():
                self.set_status(SwkBattleStatus.EscapeOver)

        elif self.status in (SwkBattleStatus.DieOver, SwkBattleStatus.EscapeOver):
            # 保持最后一帧
            pass

        self.rect.topleft = (int(self.pos_x), int(self.pos_y))

    def draw(self, surface: pygame.Surface, win_pos_x: int = 0, win_pos_y: int = 0):
        """绘制到目标表面，考虑视口偏移"""
        screen_x = int(self.pos_x - win_pos_x)
        screen_y = int(self.pos_y - win_pos_y)
        surface.blit(self.image, (screen_x, screen_y))

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.rect.topleft = (int(x), int(y))

    def move(self, dx, dy):
        """移动（用于逃跑等）"""
        self.pos_x += dx
        self.pos_y += dy
        self.rect.topleft = (int(self.pos_x), int(self.pos_y))