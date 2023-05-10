import pygame
import math
import engine.world
import os
os.environ['SDL_AUDIODRIVER'] = 'pulse'

pygame.mixer.init()


EXPLOSION_SOUND = pygame.mixer.Sound(file='src/explosion.wav')
EXPLOSION_SOUND.set_volume(0.25)


class Bullet:
    BASE_SPEED = 200
    WIDTH = 10
    HEIGHT = 10
    EXPLOSION_RADIUS = 50
    EXPLOSION_RADIUS_2 = EXPLOSION_RADIUS**2

    def __init__(self, x, y, vx, vy, px, py, fill=None, r=EXPLOSION_RADIUS):
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(vx, vy).normalize()
        self.velocity *= self.BASE_SPEED
        self.velocity.x += px
        self.velocity.y += py
        self.fill = fill
        self.radius = r
        self.collider = engine.BoxCollider(self.pos.x, self.pos.y,
                                           self.WIDTH, self.HEIGHT)

    def render(self, surf):
        pygame.draw.rect(surf, (0, 255, 0), [self.pos.x, self.pos.y, self.WIDTH, self.HEIGHT])

    def update(self, dt, world, player) -> bool:
        '''returns if the object should destruct'''
        self.pos += self.velocity*dt
        self.collider.pos += self.velocity*dt
        self.velocity.y += world.GRAVITY*dt

        # destroy after 10 seconds of falling
        if self.velocity.y >= world.GRAVITY*10:
            return True

        colliding = len(world.check_collision(self.collider)) > 0
        if colliding:
            EXPLOSION_SOUND.play()
            wx = math.floor(self.pos.x/engine.world.BLOCK_SIZE)
            wy = math.floor(self.pos.y/engine.world.BLOCK_SIZE)
            rows = world.map[max(wy-self.radius, 0): min(wy+self.radius, len(world.map))]
            # "s" in "sx" and "sy" is for slice, its not the real xy
            for sy, row in enumerate(rows):
                y = max(wy-self.radius, 0)+sy
                blocks = row[max(wx-self.radius, 0): min(wx+self.radius, len(row))]
                y_is_bad = y*engine.world.BLOCK_SIZE <= player.y+player.HEIGHT and self.fill is not None
                x_is_bad = player.x+player.WIDTH >= max(wx-self.radius, 0)*engine.world.BLOCK_SIZE and \
                    player.x <= min(wx+self.radius, len(row))*engine.world.BLOCK_SIZE
                if y_is_bad and x_is_bad:
                    continue
                for sx, block in enumerate(blocks):
                    x = max(wx-self.radius, 0)+sx
                    dist_2 = (y-wy)**2 + (x-wx)**2
                    if dist_2 <= self.radius**2:
                        world.update_block(x, y, self.fill)
                    elif dist_2 <= (self.radius+2)**2 and block is not None:
                        world.update_block(x, y, engine.Blocks.scorched_earth)
        return colliding
