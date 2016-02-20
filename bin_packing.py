# ----------------------------------------------
# CSCI 338, Spring 2016, Bin Packing Assignment
# Author: John Paxton
# Last Modified: January 25, 2016
# ----------------------------------------------
# Modified to include find_naive_solution so that
# driver does not need to be imported.  You may delete
# find_naive_solution from your submission.
# ----------------------------------------------

"""
FIND_NAIVE_SOLUTION:
    Line the the top left corners of the rectangles up along
the y = 0 axis starting with (0,0).
--------------------------------------------------
rectangles: a list of tuples, e.g. [(w1, l1), ... (wn, ln)] where
    w1 = width of rectangle 1,
    l1 = length of rectangle 1, etc.
--------------------------------------------------
RETURNS: a list of tuples that designate the top left corner placement,
         e.g. [(x1, y1), ... (xn, yn)] where
         x1 = top left x coordinate of rectangle 1 placement
         y1 = top left y coordinate of rectangle 1 placement, etc.
"""
import operator
from collections import deque
import itertools


def find_naive_solution(rectangles):
    placement = []
    upper_left_x = 0
    upper_left_y = 0

    for rectangle in rectangles:
        width = rectangle[0]
        coordinate = (upper_left_x, upper_left_y)  # make a tuple
        placement.insert(0, coordinate)  # insert tuple at front of list
        upper_left_x = upper_left_x + width

    placement.reverse()  # original order
    return placement


# -----------------------------------------------

"""
FIND_SOLUTION:
    Define this function in bin_packing.py, along with any auxiliary
functions that you need.  Do not change the driver.py file at all.
--------------------------------------------------
rectangles: a list of tuples, e.g. [(w1, l1), ... (wn, ln)] where
    w1 = width of rectangle 1,
    l1 = length of rectangle 1, etc.
--------------------------------------------------
RETURNS: a list of tuples that designate the top left corner placement,
         e.g. [(x1, y1), ... (xn, yn)] where
         x1 = top left x coordinate of rectangle 1 placement
         y1 = top left y coordinate of rectangle 1 placement, etc.
"""


# ------------------------------------------------------
#           CSCI 338, Bin Packing Assignment
#             Michael Shihrer, Jake Morison
#                   19 February 2016
# ------------------------------------------------------
#                 Solution Explanation
# ------------------------------------------------------
# First, the original order of the rectangle tuples must be saved.
#   This is necessary in order to return the results list in the original order.
# After, the rectangle tuples are sorted in decreasing order.
#   Rectangles are sorted by height.
#       If heights match, then sort by width.
# We use a tree to represent the "space" available to place items.
#   The root node represents the total size of our working space.
#       Starting size just needs to be large enough to contain the first item.
#   The tree grows.  This solves the dynamic programming problem of placing squares.
#       We use previous work (placement of rectangles) to determine where to place a new rectangle.
# For every rectangle tuple, we find an empty node large enough to fit it.
# If a node is found, child nodes are created based off the remaining space.
#   The left node represents space "below" the previously placed rectangle.
#   The right node represents space "next" to the previously placed rectangle.
# If no nodes are found that can fit a new node, we create more "space"
#   We use heuristics to guess the best way to increase space.
#       Our heuristics attempt to keep the overall working are a square.
#   Increasing space creates a new root node for the tree.
#   If space is added to the right of "full" space.
#       New space is added as a right child.
#       Otherwise, new space is added as a left child.
# This process is continued for every rectangle.
# ------------------------------------------------------
#            Benefits to this solution
# ------------------------------------------------------
#   Sorting increases the efficiency of the solution greatly.
#   Overlapping is not a concern.  We don't even have to check for it.
#   As we place larger blocks, area for smaller blocks is created.
# ------------------------------------------------------
#                   Obstacles
# ------------------------------------------------------
# Recursion is slow.
#   We optimized our solution from a runtime of about 30 seconds
#       Currently can run 10,000 items in a second or so.
# Our sort could be better.
#   Items that are much wider than they are tall should be placed a little sooner.
# ------------------------------------------------------

def find_solution(rectangles):
    sortedRectangles = []
    
    # Add original index location to rectangles - necessary for putting tuples back in order for results
    # Probably a more pythonic way to do this...
    for i, rectangle in enumerate(rectangles):
        new_tuple = rectangle + (i,)
        sortedRectangles.append(new_tuple)

    # Sort rectangles by height then width.
    # Going for a decreasing height, decreasing width best fit type of solution.
    sortedRectangles.sort(key=operator.itemgetter(1, 0), reverse=True)
    results = []

    # Create tree
    packed_tree = Tree()

    # Place sorted rectangles
    for rectangle in sortedRectangles:
        result = packed_tree.add(rectangle)
        results.append(result.rectTuple + result.coordinates)

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
    def __init__(self):
        self.root = None

    def add(self, rectangle):
        if self.root is None:                                   # Check to see if we have initialized root node
            self.root = Node(rectangle, (0, 0))                 # Root node originates at(0,0).
            empty_spaces.append(self.root)
            self.root.splitSpace(rectangle)                     # Create space for next root.
            currentNode = self.root                             # Place answer in this root.
        else:
            currentNode = self.search_spaces(rectangle)          # Find space to fit.
            if currentNode is not None:                         # Check to see if space was found.
                currentNode.splitSpace(rectangle)               # Create child nodes.
            else:
                currentNode = self.growTree(rectangle)          # No space found.  Add more.

        return currentNode                                      # Return answer.

    # Best-fit iterative search.
    @staticmethod
    def search_spaces(rectangle):
        # This is a trick to stop looping through the spaces list.
        # When spaces gets too large, it just takes too long to go through it.
        # More than likely, our best fit will be early on in the list thanks to our sorting.
        # The bigger the number, the faster our solution.  However, it becomes less accurate.
        if len(empty_spaces) > 1000:
            ignore_size = len(empty_spaces)//3
        elif len(empty_spaces) > 500:
            ignore_size = len(empty_spaces)//2
        else:
            ignore_size = len(empty_spaces)
        best_fit = None
        for space in itertools.islice(empty_spaces, 0, ignore_size):
            # See if our space is a candidate
            if space.isEmpty and (rectangle[0] <= space.rectTuple[0]) and (rectangle[1] <= space.rectTuple[1]):
                # We do!
                best_fit = space

                # Have we already found a candidate?
                if best_fit:
                    # See if our new candidate is better than the last.
                    if space.rectTuple[0] - rectangle[0] < best_fit.rectTuple[0] - rectangle[0]:
                        best_fit = space
                    elif space.rectTuple[1] - rectangle[1] < best_fit.rectTuple[1] - rectangle[1]:
                        best_fit = space

        return best_fit

    # Determine which way to grow in order to add space.
    def growTree(self, rectangle):
        goDown = rectangle[0] <= self.root.rectTuple[0]
        goRight = rectangle[1] <= self.root.rectTuple[1]

        # Sometimes it's not bad to be square.
        defGoDown = goDown and (self.root.rectTuple[0] >= (self.root.rectTuple[1] + rectangle[1]))
        defGoRight = goRight and (self.root.rectTuple[1] >= (self.root.rectTuple[0] + rectangle[0]))

        # These checks attempt to keep the working area square.
        if defGoRight:
            return self.growTreeRight(rectangle)
        elif defGoDown:
            return self.growTreeDown(rectangle)
        elif goRight:
            return self.growTreeRight(rectangle)
        elif goDown:
            return self.growTreeDown(rectangle)
        else:
            return None # this is bad.  Avoid this!

    # Create new root nodes.
    # Swap in new root.
    # Put old root in proper child.
    # I could probably generalize this...out of time
    def growTreeRight(self, rectangle):
        newRootDimensions = (self.root.rectTuple[0] + rectangle[0], self.root.rectTuple[1])
        newRoot = Node(newRootDimensions, (0, 0))
        newRoot.isEmpty = False
        newRoot.leftChild = self.root

        newRightChildSize = (rectangle[0], self.root.rectTuple[1])
        newRightChildCoords = (self.root.rectTuple[0], 0)
        newRoot.rightChild = Node(newRightChildSize, newRightChildCoords)

        self.root = newRoot

        # Right child is new. Add it to spaces only if it can fit something.
        if self.root.rightChild.rectTuple[0] > 0 and self.root.rightChild.rectTuple[1] > 0:
            empty_spaces.appendleft(newRoot.rightChild)

        self.root.rightChild.splitSpace(rectangle)
        return self.root.rightChild

    def growTreeDown(self, rectangle):
        newRootDimensions = (self.root.rectTuple[0], self.root.rectTuple[1] + rectangle[1])
        newRoot = Node(newRootDimensions, (0, 0))
        newRoot.isEmpty = False
        newRoot.rightChild = self.root

        newLeftChildSize = (self.root.rectTuple[0], rectangle[1])
        newLeftChildCoords = (0, self.root.rectTuple[1], rectangle[2])
        newRoot.leftChild = Node(newLeftChildSize, newLeftChildCoords)

        # Replace old root
        self.root = newRoot

        # Left child is new.  Add it to spaces only if it can fit something.
        if self.root.leftChild.rectTuple[0] > 0 and self.root.leftChild.rectTuple[1] > 0:
            empty_spaces.appendleft(self.root.leftChild)

        self.root.leftChild.splitSpace(rectangle)
        return self.root.leftChild


# Node represents "space"
# Can be empty or not empty.
class Node:
    def __init__(self, rectangle, coords):
        self.leftChild = None
        self.rightChild = None

        # Stores the width/height of node
        self.rectTuple = rectangle
        # Stores the upper left coordinates of node
        self.coordinates = coords
        # Just states that there is something placed in the current node.
        self.isEmpty = True

    # This splits the node and adds new child nodes
    def splitSpace(self, rect):
        # Remove space since it's no longer empty.  Might not really help since it takes time to delete.
        empty_spaces.remove(self)
        self.isEmpty = False

        # Sizes for new children
        newLeftDimen = (self.rectTuple[0], self.rectTuple[1] - rect[1])
        newRightDimen = (self.rectTuple[0] - rect[0], rect[1])

        # Starting coordinates for new children
        newLeftCoords = (self.coordinates[0], self.coordinates[1] + rect[1])
        newRightCoords = (self.coordinates[0] + rect[0], self.coordinates[1])

        # create child nodes
        self.leftChild = Node(newLeftDimen, newLeftCoords)
        self.rightChild = Node(newRightDimen, newRightCoords)

        # Add these nodes to our spaces list.
        # Only if they could possibly fit something in the future.
        # Major optimization since sometimes child nodes will have a dimension of zero
        if self.leftChild.rectTuple[0] > 0 and self.leftChild.rectTuple[1] > 0:
            empty_spaces.appendleft(self.leftChild)
        else:
            self.leftChild.isEmpty = False
        if self.rightChild.rectTuple[0] > 0 and self.rightChild.rectTuple[0] > 0:
            empty_spaces.appendleft(self.rightChild)
        else:
            self.rightChild.isEmpty = False

        # Change current node's size
        self.rectTuple = rect
