import math
import pygame


class Animation(pygame.surface.Surface):

    def __init__(self, frames, interval):
        pygame.surface.Surface.__init__(self, frames[0].get_size(), pygame.SRCALPHA, 32)
        self.frames = frames
        if isinstance(interval, list):
            self.interval = interval
        else:
            self.interval = [interval] * len(self.frames)
        self.start()

    def clear(self):
        self.fill((0,0,0,0))

    def pause(self):
        self.paused = True

    def start(self):
        self.paused = False
        self.current_frame = 0
        self.timer = self.interval[self.current_frame]
        self.clear()
        self.blit(self.frames[self.current_frame], (0, 0))

    def update(self, dt):
        if self.paused:
            return
        self.timer -= dt
        if self.timer <= 0:
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
            self.timer = self.interval[self.current_frame]
            self.clear()
            self.blit(self.frames[self.current_frame], (0, 0))
            return self.current_frame
        return None

def slice_sprite_sheet(image, tile_size_x, tile_size_y, image_x, image_y):
    sheet_width, sheet_height = image.get_size()
    width = int(sheet_width / tile_size_x)
    height = int(sheet_height / tile_size_y)
    images = [[None for j in xrange(width)] for i in xrange(height)]
    half_x = (tile_size_x - image_x)/2
    half_y = (tile_size_y - image_y)/2

    for i in xrange(height):
        for j in xrange(width):
            images[i][j] = image.subsurface(j * tile_size_x + half_x, i * tile_size_y + half_y, image_x, image_y)
    return images
