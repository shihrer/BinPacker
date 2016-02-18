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


def find_solution(rectangles):
    # How this solution works:
    # First, the original order of the rectangle tuples must be saved.
    #   This is necessary in order to return the results list in the original order.
    # After, the rectangle tuples are sorted in decreasing order.
    #   This means that the first item in the list is the "largest", followed by the next largest, down to the smallest.
    #   Largest is determined by heuristics.
    #       Experimented with width, height, area, perimeter, max(w,h)
    # We use a binary tree to represent the "space" available to place items.
    #   The root node is an arbitrary size that's large enough to fit the first item
    #       Starting size just needs to be large enough to contain the first item.
    #       Can be as big or small as that is necessary.
    # After an item is placed in the tree, that node is "used".
    # Once a node is used, child nodes are created based off the remaining space.
    #   The left node represents space "below" the previously placed rectangle.
    #   The right node represents space "next" to the previously placed rectangle.
    # This process is continued for every rectangle.
    # If no nodes are found that can fit a new node, we create more "space"
    #   We guess if it's best to place the new node below or next to the

    sortedRectangles = []
    # Add original index location to rectangles - necessary for putting tuples back in order for results
    for i, rectangle in enumerate(rectangles):
        newTuple = rectangle + (i,)
        sortedRectangles.append(newTuple)

    # Sort rectangles by height - necessary for implementing a decreasing first fit algorithm
    sortedRectangles = sorted(sortedRectangles, key=getHeightKey, reverse=True)
    results = []

    # Create tree
    binTree = Tree()
    # arbitrary size, need to make it dynamic
    binTree.root = Node((550,550),(0,0))
    # Place sorted rectangles
    for rectangle in sortedRectangles:
        result = binTree.add(rectangle)
        results.append(result.rectTuple + result.coordinates)

    # Build results list
    resultsInOriginalOrder = sorted(results, key=getOriginalIndexKey)

    # get just the results (coordinates).  Each rectangle tuple has the coordinates in indices 3&4
    # Might not need to do this...
    resultTuples = []
    for resultTuple in resultsInOriginalOrder:
        resultTuples.append((resultTuple[3], resultTuple[4]))

    return resultTuples


# Functions necessary for ordering the tuples
def getOriginalIndexKey(item):
    return item[2]


def getHeightKey(item):
    return item[1]

# Tree class for containing nodes and functions to manipulate the nodes
class Tree:
    def __init__(self):
        self.root = None
        self.emptyNodes = []

    def add(self, rectangle):
        currentNode = None
        if self.root is None:
            self.root = Node(rectangle, (0, 0))
            self.root.isEmpty = False
            self.root.splitSpace(rectangle)
            currentNode = self.root
        else:
            currentNode = self.findSpace(self.root, rectangle)
            if currentNode is not None:
                currentNode.splitSpace(rectangle)

        return currentNode

    def findSpace(self, currentNode, rectangle):
        # Replace recursion with iteration
        while currentNode is not None:
            if not currentNode.isEmpty:
                if currentNode.rectTuple[1] > rectangle[1]:
                    currentNode = currentNode.rightChild
                else:
                    currentNode = currentNode.leftChild
            elif (rectangle[0] <= currentNode.rectTuple[0]) and (rectangle[1] <= currentNode.rectTuple[1]):
                return currentNode
            else:
                currentNode = None

        # Save time by ignoring nodes that have been filled
        # for emptyNode in self.emptyNodes:
        #     if emptyNode.rectTuple[1] < rectangle[1]:
        #         currentNode = currentNode.rightChild
        #     else:
        #         currentNode = currentNode.leftChild

        # if not currentNode.isEmpty:
        #     if currentNode.rectTuple[1] < rectangle[1]:
        #         return self.findSpace(currentNode.rightChild, rectangle)
        #     else:
        #         return self.findSpace(currentNode.leftChild, rectangle)
        # elif rectangle[0] <= currentNode.rectTuple[0] and rectangle[1] <= currentNode.rectTuple[1]:
        #     return currentNode

        return currentNode


# Node represents "space"
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

    def splitSpace(self, rect):
        self.isEmpty = False

        # Sizes for children
        newLeftDimen = (self.rectTuple[0], self.rectTuple[1] - rect[1])
        newRightDimen = (self.rectTuple[0] - rect[0], rect[1])

        # Starting coordinates for children
        newLeftCoords = (self.coordinates[0], self.coordinates[1] + rect[1])
        newRightCoords = (self.coordinates[0] + rect[0], self.coordinates[1])

        #create child nodes
        self.leftChild = Node(newLeftDimen, newLeftCoords)
        self.rightChild = Node(newRightDimen, newRightCoords)

        # Change current node's size
        self.rectTuple = rect


# Represents rectangle tuples we are trying to place
class binRect:
    def __init__(self):
        self.point = binPoint()
        self.dim = ()


# Represents the top-left corner of each rectangle tuple
class binPoint:
    def __init__(self,x,y):
        self.x, self.y = x, y