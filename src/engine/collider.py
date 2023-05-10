import pygame
import math


class BoxCollider:
    def __init__(self, x, y, w, h):
        self.pos = pygame.math.Vector2(x, y)
        self.w = w
        self.h = h

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    def get_grid_indices(self, grid_size) -> (int, int, int, int):
        y_min = math.floor(self.y/grid_size)
        y_max = math.ceil((self.h+self.y)/grid_size)

        x_min = math.floor(self.x/grid_size)
        x_max = math.ceil((self.w+self.x)/grid_size)

        return (y_min, y_max, x_min, x_max)
