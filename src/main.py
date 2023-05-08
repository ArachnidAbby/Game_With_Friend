import engine
import pygame
import math


game = engine.Game()
game.world = engine.World(120, 120)
game.player = engine.Player()

game.x_off = 0
game.x_vel = False
game.y_off = 0


def render():
    game.world.render(game.window, 0, 0)
    game.player.render(game.window)


def update(dt):
    game.player.update(dt, game.world, game.window)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        game.player.velocity.x = 80
    if keys[pygame.K_a]:
        game.player.velocity.x = -80
    if keys[pygame.K_s] and not game.player.touching_ground:
        game.player.velocity.y += 100 * (game.player.velocity.y<400)*dt
    if keys[pygame.K_w] and game.player.touching_ground:
        game.player.velocity.y = -140


def events(event):
    left, middle, right = pygame.mouse.get_pressed()

    if left or right:
        block = engine.Blocks.stone if left else engine.Blocks.air
        x, y = pygame.mouse.get_pos()
        game.world.update_block(math.floor(x/5),
                                math.floor(y/5),
                                block)

if __name__ == "__main__":
    game.render = render
    game.update = update
    game.events = events
    game.start()
