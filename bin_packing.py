import operator
from collections import deque
import itertools


class Packer:
    def __init__(self):
        self.Tree = None


def find_solution(rectangles, throttle):
    sorted_rectangles = []
    
    # Add original index location to rectangles - necessary for putting tuples back in order for results
    # Probably a more pythonic way to do this...
    for i, rectangle in enumerate(rectangles):
        new_tuple = rectangle + (i,)
        sorted_rectangles.append(new_tuple)

    # Sort rectangles by height then width.
    # Going for a decreasing height, decreasing width best fit type of solution.
    sorted_rectangles.sort(key=operator.itemgetter(1, 0), reverse=True)
    results = []

    # Create tree
    packed_tree = Tree(throttle)

    # Place sorted rectangles
    for rectangle in sorted_rectangles:
        result = packed_tree.add(rectangle)
        results.append(result.rect_tuple + result.coordinates)

    # Return results to original order
    results.sort(key=operator.itemgetter(2))

    # get just the results (coordinates).  Each rectangle tuple has the coordinates in indices 3&4.
    # Make sure to set the "y" coordinate to be negative.
    result_tuples = []
    for result in results:
        result_tuples.append((result[3], -result[4]))
        
    return result_tuples

empty_spaces = deque()
# The "tree" is more of a dynamic solution for placing rectangles


class Tree:
    def __init__(self, throttle):
        self.root = None
        self.throttle = throttle
        empty_spaces.clear()

    def add(self, rectangle):
        if self.root is None:                                   # Check to see if we have initialized root node
            self.root = Node(rectangle, (0, 0))                 # Root node originates at(0,0).
            empty_spaces.append(self.root)
            self.root.split_space(rectangle)                     # Create space for next root.
            current_node = self.root                             # Place answer in this root.
        else:
            current_node = self.search_spaces(rectangle)          # Find space to fit.
            if current_node is not None:                         # Check to see if space was found.
                current_node.split_space(rectangle)               # Create child nodes.
            else:
                current_node = self.grow_tree(rectangle)          # No space found.  Add more.

        return current_node                                      # Return answer.

    # Best-fit iterative search.
    def search_spaces(self, rectangle):
        best_fit = None
        # This is a trick to stop looping through the spaces list.
        # When spaces gets too large, it just takes too long to go through it.
        # More than likely, our best fit will be early on in the list thanks to our sorting.
        # The bigger the number, the faster our solution.  However, it becomes less accurate.
        if not self.throttle:
            ignore_size = len(empty_spaces)
        elif len(empty_spaces) > 3000:
            ignore_size = len(empty_spaces) // 5
        elif len(empty_spaces) > 2000:
            ignore_size = len(empty_spaces) // 5
        elif len(empty_spaces) > 1000:
            ignore_size = len(empty_spaces) // 4
        elif len(empty_spaces) > 500:
            ignore_size = len(empty_spaces) // 2
        else:
            ignore_size = len(empty_spaces)

        for space in itertools.islice(empty_spaces, 0, ignore_size):
            # See if our space is a candidate
            if space.is_empty and (rectangle[0] <= space.rect_tuple[0]) and (rectangle[1] <= space.rect_tuple[1]):
                # We do!
                best_fit = space
                # return space

                # Have we already found a candidate?
                if best_fit:
                    # See if our new candidate is better than the last.
                    if space.rect_tuple[0] - rectangle[0] < best_fit.rect_tuple[0] - rectangle[0]:
                        best_fit = space
                    elif space.rect_tuple[1] - rectangle[1] < best_fit.rect_tuple[1] - rectangle[1]:
                        best_fit = space

        return best_fit

    # Determine which way to grow in order to add space.
    def grow_tree(self, rectangle):
        go_down = rectangle[0] <= self.root.rect_tuple[0]
        go_right = rectangle[1] <= self.root.rect_tuple[1]

        # Sometimes it's not bad to be square.
        def_go_down = go_down and (self.root.rect_tuple[0] >= (self.root.rect_tuple[1] + rectangle[1]))
        def_go_right = go_right and (self.root.rect_tuple[1] >= (self.root.rect_tuple[0] + rectangle[0]))

        # if self.root.rectTuple[0] + rectangle[0] > self.root.rectTuple[1] + rectangle[1]:
        #     defGoDown = True
        # else:
        #     defGoRight = True

        # These checks attempt to keep the working area square.
        if def_go_right:
            return self.grow_tree_right(rectangle)
        elif def_go_down:
            return self.grow_tree_down(rectangle)
        elif go_right:
            return self.grow_tree_right(rectangle)
        elif go_down:
            return self.grow_tree_down(rectangle)
        else:
            return None # this is bad.  Avoid this!

    # Create new root nodes.
    # Swap in new root.
    # Put old root in proper child.
    # I could probably generalize this...out of time
    def grow_tree_right(self, rectangle):
        new_root_dimensions = (self.root.rect_tuple[0] + rectangle[0], self.root.rect_tuple[1])
        new_root = Node(new_root_dimensions, (0, 0))
        new_root.is_empty = False
        new_root.left_child = self.root

        new_right_childsize = (rectangle[0], self.root.rect_tuple[1])
        new_right_childcoords = (self.root.rect_tuple[0], 0)
        new_root.right_child = Node(new_right_childsize, new_right_childcoords)

        self.root = new_root

        # Right child is new. Add it to spaces only if it can fit something.
        if self.root.right_child.rect_tuple[0] > 0 and self.root.right_child.rect_tuple[1] > 0:
            empty_spaces.appendleft(new_root.right_child)

        # some_node = self.search_spaces(rectangle)
        # if some_node:
        #     some_node.splitSpace(rectangle)
        #     return some_node
        # else:
        #     return None
        self.root.right_child.split_space(rectangle)
        return self.root.right_child

    def grow_tree_down(self, rectangle):
        new_root_dimensions = (self.root.rect_tuple[0], self.root.rect_tuple[1] + rectangle[1])
        new_root = Node(new_root_dimensions, (0, 0))
        new_root.is_empty = False
        new_root.right_child = self.root

        new_left_childize = (self.root.rect_tuple[0], rectangle[1])
        new_left_childcoords = (0, self.root.rect_tuple[1], rectangle[2])
        new_root.left_child = Node(new_left_childize, new_left_childcoords)

        # Replace old root
        self.root = new_root

        # Left child is new.  Add it to spaces only if it can fit something.
        if self.root.left_child.rect_tuple[0] > 0 and self.root.left_child.rect_tuple[1] > 0:
            empty_spaces.appendleft(self.root.left_child)

        # some_node = self.search_spaces(rectangle)
        # if some_node:
        #     some_node.splitSpace(rectangle)
        #     return some_node
        # else:
        #     return None
        self.root.left_child.split_space(rectangle)
        return self.root.left_child


# Node represents "space"
# Can be empty or not empty.
class Node:
    def __init__(self, rectangle, coords):
        self.left_child = None
        self.right_child = None

        # Stores the width/height of node
        self.rect_tuple = rectangle
        # Stores the upper left coordinates of node
        self.coordinates = coords
        # Just states that there is something placed in the current node.
        self.is_empty = True

    # This splits the node and adds new child nodes
    def split_space(self, rect):
        # Remove space since it's no longer empty.  Might not really help since it takes time to delete.
        empty_spaces.remove(self)
        self.is_empty = False

        # Sizes for new children
        new_left_dimen = (self.rect_tuple[0], self.rect_tuple[1] - rect[1])
        new_right_dimen = (self.rect_tuple[0] - rect[0], rect[1])

        # Starting coordinates for new children
        new_left_coords = (self.coordinates[0], self.coordinates[1] + rect[1])
        new_right_coords = (self.coordinates[0] + rect[0], self.coordinates[1])

        # create child nodes
        self.left_child = Node(new_left_dimen, new_left_coords)
        self.right_child = Node(new_right_dimen, new_right_coords)

        # Add these nodes to our spaces list.
        # Only if they could possibly fit something in the future.
        # Major optimization since sometimes child nodes will have a dimension of zero
        if self.left_child.rect_tuple[0] > 0 and self.left_child.rect_tuple[1] > 0:
            empty_spaces.appendleft(self.left_child)
        else:
            self.left_child.is_empty = False
        if self.right_child.rect_tuple[0] > 0 and self.right_child.rect_tuple[0] > 0:
            empty_spaces.appendleft(self.right_child)
        else:
            self.right_child.is_empty = False
        # Change current node's size
        self.rect_tuple = rect
