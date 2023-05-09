import pygame
import math


BLOCK_SIZE = 2


class Blocks:
    air = None
    stone = (114, 117, 115)
    scorched_earth = (92, 85, 71)

    @staticmethod
    def render(surface, block, x, y):
        if block is None:  # is air, or completely transparent
            return

        pygame.draw.rect(surface, block, (x,
                                          y,
                                          BLOCK_SIZE,
                                          BLOCK_SIZE))


FALLING_BLOCKS = (Blocks.scorched_earth, Blocks.stone)


class World:
    GRAVITY = 9.8*10
    COOLDOWN = 1/24  # 24 updates per second

    def __init__(self, width, height):
        self.map = [[Blocks.air] * width for _ in range(height)]
        self.world_surf = pygame.Surface((width*BLOCK_SIZE, height*BLOCK_SIZE)).convert()
        self.changes = []
        self.update_cooldown = 0

        for y, row in enumerate(self.map):
            if y >= height/2:
                self.map[y] = [Blocks.stone]*width

        self.render_surf()

    def render_surf(self):
        self.world_surf.fill((255, 255, 255))
        for y, row in enumerate(self.map):
            for x, block in enumerate(row):
                Blocks.render(self.world_surf, block,
                              x*BLOCK_SIZE, y*BLOCK_SIZE)

    def _update_surf(self):
        for y, x, block in self.changes:
            color = block
            if block is None:
                color = (255, 255, 255)
            pygame.draw.rect(self.world_surf, color, (x*BLOCK_SIZE,
                                                      y*BLOCK_SIZE,
                                                      BLOCK_SIZE,
                                                      BLOCK_SIZE))
        del self.changes[:]

    def render(self, surface, x_off, y_off):
        self._update_surf()
        surface.blit(self.world_surf, (x_off, y_off))

    def check_collision(self, x, y, w, h):
        rows = self.map[math.floor(y/BLOCK_SIZE):math.ceil((h+y)/BLOCK_SIZE)]
        colliding_with = []

        for by, row in enumerate(rows):
            blocks = row[math.floor(x/BLOCK_SIZE):math.ceil((w+x)/BLOCK_SIZE)]
            for bx, block in enumerate(blocks):
                if block is not None:  # ! AIR CHECK
                    colliding_with.append((bx*BLOCK_SIZE+x, by*BLOCK_SIZE+y))

        return colliding_with

    def check_rule(self, rule, x, y):
        '''
        rule = [(False, False, False),(False, False, False),(...),(False, True, True)]
        '''

    def update(self, dt):
        self.update_cooldown += dt
        if self.update_cooldown <= self.COOLDOWN:
            return

        self.update_cooldown = 0
        row_count = len(self.map)-1
        row_length =len(self.map[0])-1
        for y, row in enumerate(self.map[::-1]):
            for x, block in enumerate(row):
                under = self.map[min(row_count-y+1, row_count)][x]
                if block in FALLING_BLOCKS and under == Blocks.air:
                    self.update_block(x, row_count-y+1, block)
                    self.update_block(x, row_count-y, Blocks.air)

                # r1_2u = self.map[min(y+2, len(self.map)-1)][min(x+1, len(self.map[0])-1)]
                # r1 = 
                # l1_2u = self.map[min(y+2, len(self.map)-1)][min(x+1, len(self.map[0])-1)]

    def update_block(self, x, y, new_block):
        if y >= len(self.map):
            return
        if x >= len(self.map[0]):
            return
        self.map[y][x] = new_block
        self.changes.append((y, x, new_block))
