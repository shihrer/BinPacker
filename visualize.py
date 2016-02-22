import random

import pygame
import sys
import time
import bin_packing
from driver import read_file, corner_coordinates, find_naive_solution, evaluate_solution, is_solution_valid, \
    generate_file, generate_squares

def get_scale(screen_size, draw_size):
    screen_size_x, screen_size_y = screen_size
    draw_size_x, draw_size_y = draw_size

    x_scale = screen_size_x/draw_size_x
    y_scale = screen_size_y/draw_size_y

    return min(x_scale, y_scale)


def scale_rectangle(result, scale_factor):
    return result[0] * scale_factor, result[1] * scale_factor, result[2] * scale_factor, result[3] * scale_factor


def draw_squares(solution, perimeter):
    pygame.init()
    dflags = pygame.RESIZABLE
    size = (800, 600)
    scale_factor = get_scale(size, perimeter)
    rectangles_perimeter = (perimeter[0] + 10, perimeter[1] + 10)
    screen = pygame.display.set_mode(size, dflags)
    rectangles_surface = pygame.Surface(rectangles_perimeter)

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255,0, 0)

    screen.fill(red)
    rectangles_surface.fill(red)
    for result in solution:
        pygame.draw.rect(rectangles_surface, pastel_generator(white), result, 0)
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


def start_packer(file_name, validate, throttle, visualize, recursive):
    rectangles = read_file(file_name)
    clone = rectangles[:]  # clone so that original info retained

    # get student solution and measure tie
    start = time.time()
    upper_left_coordinates = bin_packing.find_solution(clone, throttle)
    time_elapsed = time.time() - start
    print("Time elapsed in seconds =", time_elapsed)

    # convert student solution to show upper left and lower right coordinates
    rectangle_coordinates = corner_coordinates(rectangles, upper_left_coordinates)

    # get a solution using the naive method
    naive_left_coordinates = find_naive_solution(rectangles)
    naive_rectangle_coordinates = corner_coordinates(rectangles, naive_left_coordinates)
    naive_perimeter = evaluate_solution(naive_rectangle_coordinates)
    print("Bounding Rectangle Perimeter of Naive Solution =", naive_perimeter)
    perimeter = evaluate_solution(rectangle_coordinates)
    print("Bounding Rectangle Perimeter of Your Solution =", perimeter)
    if time_elapsed > 5.0:  # is student solution fast enough?
        print("Error.  Time Limit Exceeded.")

    if validate and not is_solution_valid(rectangle_coordinates):  # is student solution valid?
        print("Error.  Overlapping Rectangles in Solution.")

    print("Percentage Improvement Over Naive Solution =", 100 - (perimeter / naive_perimeter) * 100)

    visualizeTuples = []

    tuple = upper_left_coordinates[0]  # grab first tuple of solution
    tuple2 = rectangles[0]
    global min_x, max_y, max_x, min_y

    min_x = tuple[0]  # initializing smallest x
    max_y = tuple[1]  # initializing largest y
    max_x = tuple[0]  # initializing largest x
    min_y = tuple[1]  # initializing smallest y

    for rectangle, dimension in zip(upper_left_coordinates, rectangles):
        visualizeTuples.append((rectangle[0], -rectangle[1]) + dimension)

        top_left_x = rectangle[0]
        top_left_y = rectangle[1]
        lower_right_x = rectangle[0] + dimension[0]
        lower_right_y = rectangle[1] + dimension[1]

        if top_left_x < min_x:  # find smallest x value
            min_x = top_left_x
        if lower_right_x > max_x:  # find largest x value
            max_x = lower_right_x
        if top_left_y > max_y:  # find largest y value
            max_y = top_left_y
        if lower_right_y < min_y:  # find smallest y value
            min_y = lower_right_y
    perimeter_tuple = ((max_x - min_x), (max_y - min_y))
    print(perimeter_tuple)

    if visualize:
        draw_squares(visualizeTuples, perimeter_tuple)


def pastel_generator(mix):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    if mix:
        r = (r + mix[0]) // 2
        g = (g + mix[1]) // 2
        b = (b + mix[2]) // 2

    return r, g, b

# generate parameters
file_name = "random.txt"
file_name2 = "powersof2.txt"
min_value = 1
max_value = 100
set_size = 10000

# solution parameters
validate = False
throttle = False
visualize = True
recursive = True

generate_file(file_name, min_value, max_value, set_size)
visualize_problem(file_name, validate, throttle, visualize, recursive)
