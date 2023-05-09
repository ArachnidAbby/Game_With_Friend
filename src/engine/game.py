import pygame
pygame.init()


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.update = lambda dt: 0
        self.render = lambda: 0
        self.events = lambda event: 0
        self.on_connect = lambda: 0

    def start(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self.update(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.events(event)
            if not self.running:
                break

            self.render()
            pygame.display.update()
        # * Quit Code
        pygame.quit()
        quit()
