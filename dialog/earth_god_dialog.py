# dialog/earth_god_dialog.py
import pygame
import os

class Dialog:
    def __init__(self, screen):
        """
        对话框类
        :param screen: Pygame 窗口 Surface，用于获取尺寸
        """
        self.screen = screen
        self.visible = False
        self.text = ""
        self.screen_size = screen.get_size()

        # 加载对话框背景
        dialog_path = os.path.join("resource", "img", "dialog", "dialog.png")
        self.dialog_img = pygame.image.load(dialog_path).convert_alpha()
        self.dialog_rect = self.dialog_img.get_rect()
        self.dialog_rect.width = int(self.screen_size[0] * 0.8)
        self.dialog_rect.height = int(self.dialog_rect.width * self.dialog_img.get_height() / self.dialog_img.get_width())
        self.dialog_img = pygame.transform.scale(self.dialog_img, (self.dialog_rect.width, self.dialog_rect.height))
        self.dialog_rect.center = (self.screen_size[0] // 2, self.screen_size[1] // 2)

        # 加载头像（土地公头像）
        avatar_path = os.path.join("resource", "img", "god", "1703-f9cc9fcf-00000.tga")
        try:
            self.avatar_img = pygame.image.load(avatar_path).convert_alpha()
            avatar_size = int(self.dialog_rect.height * 0.4)
            self.avatar_img = pygame.transform.scale(self.avatar_img, (avatar_size, avatar_size))
            self.avatar_rect = self.avatar_img.get_rect()
            self.avatar_rect.topleft = (self.dialog_rect.x + 20, self.dialog_rect.y + 20)
        except:
            self.avatar_img = None
            self.avatar_rect = None

        # 字体
        font_path = os.path.join("resource", "font", "newfont.TTF")
        try:
            self.font = pygame.font.Font(font_path, 18)
        except:
            self.font = pygame.font.SysFont("simsun", 18)

        # 文字区域
        self.text_rect = pygame.Rect(
            self.dialog_rect.x + 20,
            self.dialog_rect.y + 20,
            self.dialog_rect.width - 40,
            self.dialog_rect.height - 40
        )
        if self.avatar_img:
            self.text_rect.x += self.avatar_rect.width + 20
            self.text_rect.width -= self.avatar_rect.width + 20

    def show(self, text):
        """显示对话框并设置文字"""
        self.text = text
        self.visible = True

    def hide(self):
        """隐藏对话框"""
        self.visible = False

    def handle_event(self, event):
        """处理事件：按任意键关闭对话框"""
        if self.visible and event.type == pygame.KEYDOWN:
            self.hide()

    def draw(self):
        """绘制对话框（如果可见）"""
        if not self.visible:
            return
        # 绘制背景
        self.screen.blit(self.dialog_img, self.dialog_rect)
        # 绘制头像
        if self.avatar_img:
            self.screen.blit(self.avatar_img, self.avatar_rect)
        # 绘制文字
        self._blit_text()

    def _blit_text(self):
        """自动换行绘制文字"""
        words = [word.split(' ') for word in self.text.splitlines()]
        space = self.font.size(' ')[0]
        x = self.text_rect.x
        y = self.text_rect.y
        line_height = self.font.get_linesize()

        for line in words:
            for word in line:
                word_surface = self.font.render(word, True, (0, 0, 0))
                word_width, _ = word_surface.get_size()
                if x + word_width >= self.text_rect.x + self.text_rect.width:
                    x = self.text_rect.x
                    y += line_height
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = self.text_rect.x
            y += line_height