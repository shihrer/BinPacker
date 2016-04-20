import operator
import random

import time

from packer import Packer, Block
from visualize import Visualize


def generate_file(min_d, max_d, size):
    min_d = int(min_d)
    max_d = int(max_d)

    if min_d < 1:
        min_d = 1
    if max_d < 1:
        max_d = 1
    if min_d > max_d:
        temp = min_d
        min_d = max_d
        max_d = temp

    file = open("random.txt", "w")

    for rectangle in range(size):
        width = random.randint(min_d, max_d)
        height = random.randint(min_d, max_d)
        file.write("{} {}\n".format(width, height))

    file.close()


def read_file(name):
    file = open(name, "r")
    next_line = file.readline()
    rectangles = []

    while next_line:
        dimensions = next_line.split()
        dimensions = (int(dimensions[0]), int(dimensions[1]))
        rectangles.append(dimensions)
        next_line = file.readline()

    return rectangles


def overlap(a, b):
    return not (b.location[0] >= a.location[0] + a.size[0] or
                b.location[0] + b.size[0] <= a.location[0] or
                b.location[1] >= a.location[1] + a.size[1] or
                b.location[1] + b.size[1] <= a.location[1])


def check_solution(results):
    for i, a in enumerate(results):
        for j, b in enumerate(results[i + 1:]):
            if overlap(a, b):
                return False

    return True


def find_perimeter(results):
    max_y, max_x = 0, 0

    for result in results:
        low_x = result.location[0] + result.size[0]
        low_y = result.location[1] + result.size[1]

        if low_x > max_x:
            max_x = low_x
        if low_y > max_y:
            max_y = low_y

    return SolutionBounds((max_x, max_y))


def naive_solution(rectangles):
    x, y = 0, 0
    naive_results = []

    for rectangle in rectangles:
        coordinate = (x, y)
        naive_results.append(Block(coordinate, rectangle))
        x = x + rectangle[0]

    return naive_results


def find_solution(rectangles):
    # Rotate
    # for i, rectangle in enumerate(rectangles):
    #     if rectangle[0] > rectangle[1]:
    #         rectangles[i] = (rectangle[1], rectangle[0])

    # Sort by height, then width
    rectangles.sort(key=operator.itemgetter(1, 0), reverse=True)
    return Packer.pack(Packer(), rectangles)


class SolutionBounds():
    def __init__(self, dimensions):
        self.dimensions = dimensions

    def get_perimeter(self):
        return (self.dimensions[0] + self.dimensions[1]) * 2


def run_random():
    # generate_file(1, 100, 10000)
    rectangles = read_file("random.txt")

    naive_results = naive_solution(rectangles)

    start = time.time()
    my_results = find_solution(rectangles)
    time_elapsed = time.time() - start

    print("Solution ran in {} seconds".format(time_elapsed))

    # This is slow
    # if not check_solution(my_results):
    #     print("Solution invalid.  Overlap detected.")

    solution_space = find_perimeter(my_results)
    naive_space = find_perimeter(naive_results)

    print("Dimensions of solution are {}.".format(solution_space.dimensions))
    print("Perimeter of solution is {}.".format(solution_space.get_perimeter()))
    print("Dimensions of naive solution are {}.".format(naive_space.dimensions))
    print("Perimeter of naive solution is {}.".format(naive_space.get_perimeter()))
    print("Percentage improvement is {}.".format(
        (100 - (solution_space.get_perimeter() / naive_space.get_perimeter()) * 100)))

    visualizer = Visualize(my_results, solution_space)
    # visualizer.display()


def run_tests():
    total_improvement = 0
    file_count = 70
    for i in range(1, file_count + 1):

        rectangles = read_file("data/{}.in".format(i))
        naive_results = naive_solution(rectangles)

        start = time.time()
        my_results = find_solution(rectangles)
        time_elapsed = time.time() - start

        # This is slow
        # if not check_solution(my_results):
        #     print("Solution invalid.  Overlap detected.")

        solution_space = find_perimeter(my_results)
        naive_space = find_perimeter(naive_results)
        improvement = naive_space.get_perimeter() / solution_space.get_perimeter()

        print("Test {} ran in {} seconds for improvement of {}.  {}".format(i, time_elapsed, improvement, solution_space.dimensions))
        total_improvement += improvement

    print("Overall improvement is {}.".format(total_improvement/file_count))


# Runs the code.
if __name__ == "__main__":
    run_random()
