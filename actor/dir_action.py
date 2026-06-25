import pygame
import os

class DirAction:
    def __init__(self, path_name1: str, path_name2: str, prefix: str,
                 dir_count: int, frame_count: int, is_loop: bool = True,
                 filename_template: str = "{prefix}{d:02d}{f:02d}.tga"):
        self.dir_count = dir_count
        self.frame_count = frame_count
        self.is_loop = is_loop
        self.current_dir = 0
        self.frame_index = 0

        self.frames = []
        for d in range(dir_count):
            dir_frames = []
            for f in range(frame_count):
                filename = filename_template.format(prefix=prefix, d=d, f=f)
                img_path = os.path.join("resource", path_name1, path_name2, filename)
                img = pygame.image.load(img_path).convert_alpha()
                dir_frames.append(img)
            self.frames.append(dir_frames)

        self.image = self.frames[self.current_dir][self.frame_index]

    def set_direction(self, dir_index: int):
        if 0 <= dir_index < self.dir_count:
            self.current_dir = dir_index
            self.image = self.frames[self.current_dir][self.frame_index]

    def update(self):
        if self.is_loop:
            self.frame_index = (self.frame_index + 1) % self.frame_count
        else:
            if self.frame_index < self.frame_count - 1:
                self.frame_index += 1
        self.image = self.frames[self.current_dir][self.frame_index]

    def get_current_image(self):
        return self.image

    def is_end(self):
        if self.is_loop:
            return False
        return self.frame_index >= self.frame_count - 1

    def reset(self):
        self.frame_index = 0
        self.image = self.frames[self.current_dir][self.frame_index]