import random

import pygame
import sys
import time
from Packer import Packer

class Visualizer:
    def __init__(self):
        self.packer = Packer(throttle)

    def get_scale(self, screen_size, draw_size):
        screen_size_x, screen_size_y = screen_size
        draw_size_x, draw_size_y = draw_size

        x_scale = screen_size_x / draw_size_x
        y_scale = screen_size_y / draw_size_y

        return min(x_scale, y_scale)

    def draw_squares(self, solution, perimeter):
        pygame.init()
        dflags = pygame.RESIZABLE
        size = (800, 600)
        scale_factor = self.get_scale(size, perimeter)
        rectangles_perimeter = (perimeter[0] + 10, perimeter[1] + 10)
        screen = pygame.display.set_mode(size, dflags)
        rectangles_surface = pygame.Surface(rectangles_perimeter)

        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)

        screen.fill(red)
        rectangles_surface.fill(red)
        for result in solution:
            pygame.draw.rect(rectangles_surface, self.pastel_generator(white), result, 0)
            pygame.draw.rect(rectangles_surface, black, result, 1)

        while True:
            # check for quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    size = event.dict['size']
                    screen = pygame.display.set_mode(size, dflags)

            screen.fill(red)
            if rectangles_perimeter > size:
                screen.blit(pygame.transform.smoothscale(rectangles_surface, size), (0, 0))
            else:
                screen.blit(rectangles_surface, (0, 0))

            # update the screen
            pygame.display.update()

    @staticmethod
    def pastel_generator(mix):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        if mix:
            r = (r + mix[0]) // 2
            g = (g + mix[1]) // 2
            b = (b + mix[2]) // 2

        return r, g, b
