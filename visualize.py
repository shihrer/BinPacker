import pygame
import random
import time

import sys

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)


def pastel_mixer(mix):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    if mix:
        r = (r + mix[0]) // 2
        g = (g + mix[1]) // 2
        b = (b + mix[2]) // 2

    return r, g, b


class Visualize:
    def __init__(self, blocks, solution_space):
        self.size = (800, 600)
        self.dflags = pygame.RESIZABLE
        self.blocks = blocks
        self.solution_space = solution_space
        self.screen = pygame.display.set_mode(self.size, self.dflags)
        self.rectangles_surface = pygame.Surface(self.solution_space.dimensions)

    def display(self):
        pygame.init()

        self.screen.fill(red)
        self.rectangles_surface.fill(red)

        self.draw_squares()
        while True:
            # check for quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.size = event.dict['size']
                    self.screen = pygame.display.set_mode(self.size, self.dflags)

            # update the screen
            self.update_screen()

    def get_scale(self):
        pass

    def draw_squares(self):
        for block in self.blocks:
            pygame.draw.rect(self.rectangles_surface, pastel_mixer(white), block.rect, 0)
            pygame.draw.rect(self.rectangles_surface, black, block.rect, 1)

    def update_screen(self):
        self.screen.fill(red)
        if self.solution_space.dimensions > self.size:
            self.screen.blit(pygame.transform.smoothscale(self.rectangles_surface, self.size), (0, 0))
        else:
            self.screen.blit(self.rectangles_surface, (0, 0))

        pygame.display.update()
