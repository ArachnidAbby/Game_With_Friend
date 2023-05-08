import pygame
import math


BLOCK_SIZE = 5


class Blocks:
    air = None
    stone = (114, 117, 115)

    @staticmethod
    def render(surface, block, x, y):
        if block is None:  # is air, or completely transparent
            return

        pygame.draw.rect(surface, block, (x,
                                          y,
                                          BLOCK_SIZE,
                                          BLOCK_SIZE))


class World:
    def __init__(self, width, height):
        self.map = [[Blocks.air] * width for _ in range(height)]

        for y, row in enumerate(self.map):
            if y >= height/2:
                self.map[y] = [Blocks.stone]*width

    def render(self, surface, x_off, y_off):
        for y, row in enumerate(self.map):
            for x, block in enumerate(row):
                Blocks.render(surface, block,
                              x*BLOCK_SIZE + x_off, y*BLOCK_SIZE + y_off)

    def check_collision(self, x, y, w, h):
        rows = self.map[math.floor(y/BLOCK_SIZE):math.ceil((h+y)/BLOCK_SIZE)]
        colliding_with = []

        for by, row in enumerate(rows):
            blocks = row[math.floor(x/BLOCK_SIZE):math.ceil((w+x)/BLOCK_SIZE)]
            for bx, block in enumerate(blocks):
                if block is not None:  # ! AIR CHECK
                    colliding_with.append((bx*BLOCK_SIZE+x, by*BLOCK_SIZE+y))

        return colliding_with

    def update(self, dt):
        pass

    def update_block(self, x, y, new_block):
        if y >= len(self.map):
            return
        if x >= len(self.map[0]):
            return
        self.map[y][x] = new_block
