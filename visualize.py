import pygame
import sys
import time
import bin_packing
from driver import read_file, corner_coordinates, find_naive_solution, evaluate_solution, is_solution_valid, \
    generate_file

min_x = 0
max_y = 0
max_x = 0
min_y = 0

def visualize_problem(file_name):
    rectangles = read_file(file_name)
    clone = rectangles[:]       # clone so that original info retained

    # get student solution and measure tie
    start = time.time()
    upper_left_coordinates = bin_packing.find_solution(clone)
    time_elapsed = time.time() - start
    print("Time elapsed in seconds =", time_elapsed)

    # convert student solution to show upper left and lower right coordinates
    rectangle_coordinates = corner_coordinates(rectangles, upper_left_coordinates)

    # get a solution using the naive method
    naive_left_coordinates = find_naive_solution(rectangles)
    naive_rectangle_coordinates = corner_coordinates(rectangles, naive_left_coordinates)
    naive_perimeter = evaluate_solution(naive_rectangle_coordinates)
    print("Bounding Rectangle Perimeter of Naive Solution =", naive_perimeter)


    if is_solution_valid (rectangle_coordinates):   # is student solution valid?
        perimeter = evaluate_solution(rectangle_coordinates)
        print("Bounding Rectangle Perimeter of Your Solution =", perimeter)
        if time_elapsed > 5.0:                      # is student solution fast enough?
            print("Error.  Time Limit Exceeded.")
            # perimeter = 2 * naive_perimeter         # answer is penalized

    else:
        print("Error.  Overlapping Rectangles in Solution.")
        perimeter = 2 * naive_perimeter             # answer is penalized

    print("Percentage Improvement Over Naive Solution =", 100 - (perimeter / naive_perimeter) * 100)

    visualizeTuples = []

    tuple = upper_left_coordinates[0]              # grab first tuple of solution
    tuple2 = rectangles[0]
    global min_x, max_y, max_x, min_y

    min_x = tuple[0]                    # initializing smallest x
    max_y = tuple[1]                    # initializing largest y
    max_x = tuple[0]                    # initializing largest x
    min_y = tuple[1]                    # initializing smallest y

    for rectangle, dimension in zip(upper_left_coordinates, rectangles):
        visualizeTuples.append((rectangle[0], -rectangle[1]) + dimension)

        top_left_x = rectangle[0]
        top_left_y = rectangle[1]
        lower_right_x = rectangle[0] + dimension[0]
        lower_right_y = rectangle[1] + dimension[1]

        if top_left_x < min_x:          # find smallest x value
            min_x = top_left_x
        if lower_right_x > max_x:       # find largest x value
            max_x = lower_right_x
        if top_left_y > max_y:          # find largest y value
            max_y = top_left_y
        if lower_right_y < min_y:       # find smallest y value
            min_y = lower_right_y

    return visualizeTuples

# for i in range(1,70):
#     generate_file("squares.txt", 1, 1000, 10000)
#     rectangles = visualize_problem("squares.txt")


generate_file("squares.txt", 1, 1000, 100)
rectangles = visualize_problem("squares.txt")

pygame.init()
dflags = pygame.RESIZABLE
size = (800,600)
rectangles_perimeter = ((max_x - min_x) + 50, (max_y - min_y) + 50)
screen = pygame.display.set_mode(size, dflags)
rectangles_surface = pygame.Surface(rectangles_perimeter)

print (rectangles_perimeter)

red = (255,0,0)
white = (255,255,255)

while True:
    # check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();
        if event.type == pygame.VIDEORESIZE:
            size = event.dict['size']
            screen = pygame.display.set_mode(size, dflags)

    rectangles_surface.fill(white)

    for rectangle in rectangles:
        pygame.draw.rect(rectangles_surface, red, rectangle, 1)

    screen.blit(pygame.transform.smoothscale(rectangles_surface, size), (0, 0))

    # update the screen
    pygame.display.update()