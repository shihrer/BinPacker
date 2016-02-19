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
import time
from collections import deque


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
#   This means that the first item in the list is the "largest"
#       Followed by the next largest, down to the smallest.
#   Largest is determined by heuristics.
#       Experimented with width, height, area, perimeter, max(w,h).
# We use a binary tree to represent the "space" available to place items.
#   The root node represents the total size of our working space.
#       Starting size just needs to be large enough to contain the first item.
# For every rectangle tuple, we find an empty node large enough to fit it.
# If a node is found, child nodes are created based off the remaining space.
#   The left node represents space "below" the previously placed rectangle.
#   The right node represents space "next" to the previously placed rectangle.
# If no nodes are found that can fit a new node, we create more "space"
#   We use heuristics to guess the best way to increase space.
#   Increasing space creates a new root node for the tree.
#   If space is added to the right of "full" space.
#       New space is added as a right child.
#       Otherwise, new space is added as a left child.
# This process is continued for every rectangle.
# ------------------------------------------------------
#            Benefits to this solution
# ------------------------------------------------------
#   Sorting increases the efficiency of the solution greatly.
#   Overlapping is not a concern with sorted results.
#   As we place larger blocks, area for smaller blocks is created.
#   After a certain point, small blocks can be placed without increasing our working area.
# ------------------------------------------------------
#                   Obstacles
# ------------------------------------------------------
# Recursion is slow.
# ------------------------------------------------------
spaces = deque()

def find_solution(rectangles):
    sortedRectangles = []
    
    # Add original index location to rectangles - necessary for putting tuples back in order for results
    for i, rectangle in enumerate(rectangles):
        newTuple = rectangle + (i,)
        sortedRectangles.append(newTuple)

    # Sort rectangles by height - necessary for implementing a decreasing first fit type of solution
    sortedRectangles.sort(key=getHeightKey, reverse=True)
    results = []

    # Create tree
    binTree = Tree()

    start = time.time()
    # Place sorted rectangles
    for rectangle in sortedRectangles:
        result = binTree.add(rectangle)
        results.append(result.rectTuple + result.coordinates)
    time_elapsed = time.time() - start
    print("My solution ran in =", time_elapsed)

    # Return results to original order
    results.sort(key=getOriginalIndexKey)

    # get just the results (coordinates).  Each rectangle tuple has the coordinates in indices 3&4.
    # Make sure to set the "y" coordinate to be negative.
    resultTuples = []
    for resultTuple in results:
        resultTuples.append((resultTuple[3], -resultTuple[4]))
        
    resultTuples = []
    for resultTuple in results:
        resultTuples.append((resultTuple[3], -resultTuple[4]))
        
    return resultTuples


# Functions necessary for ordering the tuples
def getHeightKey(item):
    return item[1]

def getMaxSide(item):
    if item[0] > item[1]:
        return item[0]
    else:
        return item[1]

def getWidthKey(item):
    return item[0]


def getOriginalIndexKey(item):
    return item[2]

def getMaxSide(item):
    if item[0] > item[1]:
        return item[0]
    else:
        return item[1]


# Tree class for containing nodes and functions to manipulate the nodes
class Tree:
    def __init__(self):
        self.root = None

    def add(self, rectangle):
        currentNode = None                                      # Setup variable to return answer.
        if self.root is None:                                   # Check to see if we have initialized root node
            self.root = Node(rectangle, (0, 0))                 # Root node originates at(0,0).
            spaces.append(self.root)
            self.root.splitSpace(rectangle)                     # Create space for next root.
            currentNode = self.root                             # Place answer in this root.
        else:
            # start = time.time()
            #currentNode = self.findSpaceDFS(rectangle)
            currentNode = self.searchSpaces(rectangle)
            # time_elapsed = time.time() - start
            # print("DFS in = ", time_elapsed)
            # start = time.time()
            # currentNode = self.findSpace(self.root, rectangle)  # Find space to fit.
            # time_elapsed = time.time() - start
            # print("Normal in =", time_elapsed)
            #print("DFS processed = ", len(test))
            if currentNode is not None:                         # Check to see if space was found.
                currentNode.splitSpace(rectangle)               # Create child nodes.
            else:
                currentNode = self.growTree(rectangle)          # No space found.  Add more.


        return currentNode                                      # Return answer.

    def searchSpaces(self, rectangle):
        for space in spaces:
            if space.isEmpty and (rectangle[0] <= space.rectTuple[0]) and (rectangle[1] <= space.rectTuple[1]):
                return space
        return None

    def findSpaceDFS(self, rectangle):
        visited, stack = set(), deque([self.root])
        while stack:
            current = stack.popleft()
            if current in visited:
                continue

            visited.add(current)
            if current.leftChild is not None:
                node_children = set([current.leftChild, current.rightChild])
                stack.extend(node_children - visited)

            if current.isEmpty and (rectangle[0] <= current.rectTuple[0]) and (rectangle[1] <= current.rectTuple[1]):
                return current

        return None

    def basic_dfs(self, currentNode, rectangle):
        # if not currentNode.isEmpty:
        #     return self.findSpace(currentNode.rightChild, rectangle) or self.findSpace(currentNode.leftChild, rectangle)
        # elif (rectangle[0] <= currentNode.rectTuple[0] and rectangle[1] <= currentNode.rectTuple[1]):
        #     return currentNode
        # else:
        #     return None

        if not currentNode.isEmpty:
            yield

        return None

    def findSpace(self, currentNode, rectangle):


        # traversalStack = []
        # currentNode = self.root
        # done = 0
        #
        # while not done:
        #     # if currentNode is not None and currentNode.isEmpty:
        #     #     if (rectangle[0] <= currentNode.rectTuple[0]) and (rectangle[1] <= currentNode.rectTuple[1]):
        #     #         return currentNode
        #
        #     if currentNode is not None:
        #         traversalStack.append(currentNode)
        #         currentNode = currentNode.rightChild
        #     else:
        #         if len(traversalStack) > 0:
        #             currentNode = traversalStack.pop()
        #             if currentNode.isEmpty and (rectangle[0] <= currentNode.rectTuple[0]) and (rectangle[1] <= currentNode.rectTuple[1]):
        #                 return currentNode
        #             currentNode = currentNode.leftChild
        #         else:
        #             done = 1
        # current = self.root
        # parents = []
        # def descend_right(current):
        #     while current is not None:
        #         parents.append(current)
        #         current = currentNode.rightChild
        # descend_right(current)
        # while parents:
        #     current = parents.pop()
        #     if current.isEmpty and (rectangle[0] <= current.rectTuple[0]) and (rectangle[1] <= current.rectTuple[1]):
        #         return current
        #
        #     descend_right(current.leftChild)



        if not currentNode.isEmpty:
            return self.findSpace(currentNode.rightChild, rectangle) or self.findSpace(currentNode.leftChild, rectangle)
        elif (rectangle[0] <= currentNode.rectTuple[0] and rectangle[1] <= currentNode.rectTuple[1]):
            return currentNode
        else:
            return None

        # Recursively check our tree - optimize
        # if currentNode is None:
        #     return None
        # if currentNode.isEmpty and rectangle[0] <= currentNode.rectTuple[0] and rectangle[1] <= currentNode.rectTuple[1]:
        #     return currentNode
        # elif not currentNode.isEmpty:
        #     # someNode = self.findSpace(currentNode.rightChild, rectangle)
        #     # somenode2 = self.findSpace(currentNode.leftChild, rectangle)
        #     # return someNode or somenode2
        #     # if someNode:
        #     #     return someNode
        #     # else:
        #     #     return self.findSpace(currentNode.leftChild, rectangle)
        #
        #     # if someNode and somenode2:
        #     #     return someNode
        #     # elif not someNode:
        #     #     if somenode2:
        #     #         return somenode2
        #     # elif not somenode2:
        #     #     if someNode:
        #     #         return someNode
        #     return self.findSpace(currentNode.rightChild, rectangle) or self.findSpace(currentNode.leftChild, rectangle)

        return None

    # Heuristic function for determining best way to add empty space.
    def growTree(self, rectangle):
        # These two checks attempt to keep the working area square.
        if self.root.rectTuple[1] < self.root.rectTuple[0]:
            return self.growTreeDown(rectangle)
        else:
            return self.growTreeRight(rectangle)

    # Pretty boring functions.
    # Create new root nodes.
    # Swap in new root.
    # Put old root in proper child.
    def growTreeRight(self, rectangle):
        newRootDimensions = (self.root.rectTuple[0] + rectangle[0], self.root.rectTuple[1])
        newRoot = Node(newRootDimensions, (0, 0))
        newRoot.isEmpty = False
        newRoot.leftChild = self.root

        newRightChildSize = (rectangle[0], self.root.rectTuple[1])
        newRightChildCoords = (self.root.rectTuple[0], 0)
        newRoot.rightChild = Node(newRightChildSize, newRightChildCoords)

        self.root = newRoot
        spaces.append(newRoot)
        spaces.append(self.root.rightChild)
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

        self.root = newRoot
        spaces.append(newRoot)
        spaces.append(self.root.leftChild)
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

    # def __key(self):
    #     return self.coordinates
    #
    # def __hash__(self):
    #     return hash(self.coordinates)
    #
    # def __eq__(x,y):
    #     return x.__key() == y.__key()

    def splitSpace(self, rect):
        #spaces.remove(self)
        self.isEmpty = False

        # Sizes for children
        newLeftDimen = (self.rectTuple[0], self.rectTuple[1] - rect[1])
        newRightDimen = (self.rectTuple[0] - rect[0], rect[1])

        # Starting coordinates for children
        newLeftCoords = (self.coordinates[0], self.coordinates[1] + rect[1])
        newRightCoords = (self.coordinates[0] + rect[0], self.coordinates[1])

        # create child nodes
        self.leftChild = Node(newLeftDimen, newLeftCoords)
        self.rightChild = Node(newRightDimen, newRightCoords)
        spaces.extendleft([self.leftChild, self.rightChild])

        # Change current node's size
        self.rectTuple = rect


# Represents rectangle tuples we are trying to place
class binRect:
    def __init__(self):
        self.point = binPoint()
        self.dim = ()


# Represents the top-left corner of each rectangle tuple
class binPoint:
    def __init__(self, x, y):
        self.x, self.y = x, y
