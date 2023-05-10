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
        self.body_collider = engine.BoxCollider(self.x,
                                                self.y+1,
                                                self.WIDTH,
                                                self.HEIGHT-11)

        self.foot_collider = engine.BoxCollider(self.x+1,
                                                self.y+self.HEIGHT-10,
                                                self.WIDTH-2,
                                                10)
        self.ground_collider = engine.BoxCollider(self.x+1,
                                                  self.y+self.HEIGHT+1,
                                                  self.WIDTH-2,
                                                  0)
        self.head_collider = engine.BoxCollider(self.x+1,
                                                self.y-1,
                                                self.WIDTH-2,
                                                5)
        # end of __init__

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

    def add_to_y(self, val):
        self.pos.y += val
        self.body_collider.pos.y += val
        self.foot_collider.pos.y += val
        self.ground_collider.pos.y += val
        self.head_collider.pos.y += val

    def add_to_x(self, val):
        self.pos.x += val
        self.body_collider.pos.x += val
        self.foot_collider.pos.x += val
        self.ground_collider.pos.x += val
        self.head_collider.pos.x += val

    def calc_intersections(self, dt, intersected_with):
        right_edge = self.WIDTH + self.x
        left_edge = self.x
        center = self.WIDTH/2 + self.x
        prev_x = self.x
        for x, y in intersected_with:
            if x > center:
                if self.velocity.x > 0:
                    self.velocity.x = 0
                self.add_to_x(min(self.x, prev_x+(right_edge - x) * dt)-self.x)
            if x+engine.world.BLOCK_SIZE < center:
                val = (left_edge-(x+engine.world.BLOCK_SIZE))
                if self.velocity.x < 0:
                    self.velocity.x = 0
                self.add_to_x(max(self.x, prev_x - val*dt)-self.x)

    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), [self.pos.x,
                                                math.ceil(self.pos.y),
                                                self.WIDTH,
                                                self.HEIGHT])

    def update(self, dt, world, surf):
        self.velocity.y += world.GRAVITY*dt
        self.velocity -= self.velocity*self.FRICTION*dt

        self.touching_ground = len(world.check_collision(self.ground_collider)) > 0
        if self.touching_ground and self.velocity.y > 0:
            self.velocity.y = 0
        if self.touching_ground:
            self.velocity.x -= self.velocity.x*self.GROUND_FRIC*dt

        intersected_with = world.check_collision(self.body_collider)
        touching_foot = len(world.check_collision(self.foot_collider)) > 0
        head_touching = len(world.check_collision(self.head_collider)) > 0

        if head_touching and self.velocity.y < 0:
            self.velocity.y = 0

        if touching_foot and len(intersected_with) > 0 and \
                self.touching_ground and head_touching:
            self.velocity.y = world.GRAVITY * -0.5
        else:
            self.calc_intersections(dt, intersected_with)

        if touching_foot and len(intersected_with) == 0:
            self.add_to_y(-1 * min(max(self.velocity.x, 5), 1))
            self.velocity -= self.velocity*self.FRICTION*2*dt

        self.pos += self.velocity * dt
        self.body_collider.pos += self.velocity * dt
        self.foot_collider.pos += self.velocity * dt
        self.ground_collider.pos += self.velocity * dt
        self.head_collider.pos += self.velocity * dt
