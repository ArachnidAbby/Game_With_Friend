import engine
import pygame
import math


COOLDOWN_TIME = 0.14
RENDER_COOLDOWN = 1/60

game = engine.Game()
game.world = engine.World(int(600/engine.world.BLOCK_SIZE), int(600/engine.world.BLOCK_SIZE))
game.player = engine.Player()
game.bullet_cooldown = 0
game.render_cooldown = 0

game.bullets = []


def render():
    # if game.render_cooldown < RENDER_COOLDOWN:
        # return

    game.window.fill((255, 255, 255))
    game.world.render(game.window, 0, 0)
    for bullet in game.bullets:
        bullet.render(game.window)
    game.player.render(game.window)


def update(dt):
    game.render_cooldown += dt
    game.bullet_cooldown += dt

    c = 0
    while c < len(game.bullets):
        bullet = game.bullets[c]
        if bullet.update(dt, game.world, game.player):
            del game.bullets[c]
            continue
        c += 1

    game.world.update(dt)

    game.player.update(dt, game.world, game.window)

    keys = pygame.key.get_pressed()
    divider = 1+(not game.player.touching_ground)/2
    if keys[pygame.K_d]:
        game.player.velocity.x = 60/divider
    if keys[pygame.K_a]:
        game.player.velocity.x = -60/divider
    if keys[pygame.K_s] and not game.player.touching_ground:
        game.player.velocity.y += 100 * (game.player.velocity.y < 400)*dt
    if keys[pygame.K_w] and game.player.touching_ground:
        game.player.velocity.y = -140


def events(event):
    left, middle, right = pygame.mouse.get_pressed()

    if left:
        block = engine.Blocks.stone if left else engine.Blocks.air
        x, y = pygame.mouse.get_pos()
        game.world.update_block(math.floor(x/engine.world.BLOCK_SIZE),
                                math.floor(y/engine.world.BLOCK_SIZE),
                                block)

    if right and game.bullet_cooldown >= COOLDOWN_TIME:
        game.bullet_cooldown = 0
        x, y = pygame.mouse.get_pos()
        bullet = engine.Bullet(game.player.x,
                               game.player.y,
                               x-game.player.x,
                               y-game.player.y,
                               game.player.vx,
                               game.player.vy,
                               fill=engine.world.Blocks.stone, r=30)
        game.bullets.append(bullet)

    if middle and game.bullet_cooldown >= COOLDOWN_TIME:
        game.bullet_cooldown = 0
        x, y = pygame.mouse.get_pos()
        bullet = engine.Bullet(game.player.x,
                               game.player.y,
                               x-game.player.x,
                               y-game.player.y,
                               game.player.vx,
                               game.player.vy)
        game.bullets.append(bullet)


if __name__ == "__main__":
    game.render = render
    game.update = update
    game.events = events
    game.start()
