import pygame
import sys
import time
import bin_packing
from driver import read_file, corner_coordinates, find_naive_solution, evaluate_solution, is_solution_valid, \
    generate_file


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
    for rectangle, dimension in zip(upper_left_coordinates, rectangles):
        visualizeTuples.append((rectangle[0], -rectangle[1]) + dimension)

    return visualizeTuples


pygame.init()

screen = pygame.display.set_mode((1024,768))

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

generate_file("squares.txt", 5, 20, 1000)
rectangles = visualize_problem("squares2.txt")

while True:
    # check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();

    screen.fill(white)

    for rectangle in rectangles:
        pygame.draw.rect(screen, red, rectangle, 1)

    # update the screen
    pygame.display.update()