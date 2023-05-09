import pygame
import engine.world
import math


class Player:
    FRICTION = 0.05
    GROUND_FRIC = 3

    HEIGHT = 50
    WIDTH = 20

    def __init__(self):
        self.pos = pygame.math.Vector2(300, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.touching_ground = False

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    @property
    def vx(self):
        return self.velocity.x

    @property
    def vy(self):
        return self.velocity.y

    def calc_intersections(self, dt, intersected_with):
        right_edge = self.WIDTH + self.pos.x
        left_edge = self.pos.x
        center = self.WIDTH/2 + self.pos.x
        prev_x = self.pos.x
        for x, y in intersected_with:
            if x > center:
                if self.velocity.x > 0:
                    self.velocity.x = 0
                self.pos.x = min(self.pos.x, prev_x+(right_edge - x) * dt)
            if x+engine.world.BLOCK_SIZE < center:
                val = (left_edge-(x+engine.world.BLOCK_SIZE))
                if self.velocity.x < 0:
                    self.velocity.x = 0
                self.pos.x = max(self.pos.x, prev_x - val*dt)

    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), [self.pos.x, math.ceil(self.pos.y), self.WIDTH, self.HEIGHT])

    def update(self, dt, world, surf):
        self.velocity.y += world.GRAVITY*dt
        self.velocity -= self.velocity*self.FRICTION*dt

        self.touching_ground = len(world.check_collision(self.pos.x+1, self.pos.y+self.HEIGHT+1, self.WIDTH-2, 0)) > 0
        if self.touching_ground and self.velocity.y > 0:
            self.velocity.y = 0
        if self.touching_ground:
            self.velocity.x -= self.velocity.x*self.GROUND_FRIC*dt

        intersected_with = world.check_collision(self.pos.x, self.pos.y+1, self.WIDTH, self.HEIGHT-11)
        touching_foot = len(world.check_collision(self.pos.x+1, self.pos.y+self.HEIGHT-10, self.WIDTH-2, 10)) > 0
        head_touching = len(world.check_collision(self.pos.x+1, self.pos.y-1, self.WIDTH-2, 5)) > 0

        if head_touching and self.velocity.y<0:
            self.velocity.y = 0

        if touching_foot and len(intersected_with) > 0 and self.touching_ground and head_touching:
            self.velocity.y = world.GRAVITY * -0.5
        else:
            self.calc_intersections(dt, intersected_with)

        if touching_foot and len(intersected_with) == 0:
            self.pos.y-= min(max(self.velocity.x, 5), 1)
            self.velocity -= self.velocity*self.FRICTION*2*dt


        self.pos += self.velocity * dt
