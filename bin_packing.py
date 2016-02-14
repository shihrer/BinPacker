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

def find_naive_solution (rectangles):   
    placement = []
    upper_left_x = 0
    upper_left_y = 0
    
    for rectangle in rectangles:
        width = rectangle[0]
        coordinate = (upper_left_x, upper_left_y)   # make a tuple
        placement.insert(0, coordinate)             # insert tuple at front of list
        upper_left_x = upper_left_x + width
        
    placement.reverse()                             # original order
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
    sortedRectangles = []
    #Add original index location to rectangles
    for i, rectangle in enumerate(rectangles):
        testTuple = rectangle + (i,)
        sortedRectangles.append(testTuple)
    sortedRectangles = sorted(sortedRectangles, key=getHeightKey, reverse = True)

    # Root node is first node in sorted list.
    rootNode = Node(sortedRectangles[0])

    # GO through each rectangle in sorted list and find a space for it to fit into.
    # for rectangle in sortedRectangles:
    #
    #     if findSpace(rootNode, rectangle):
    #         #Found space, cut remaining white space in two and save to tree
    #         cutSpace()
    #     else:
    #         #Space not found.  Grow our rectangle to accommodate.
    #         increaseSpace()

    originalOrderRectangles = sorted(sortedRectangles, key=getOriginalIndexKey)
    return None

#Recursively search through tree to find space for new rectangle
def findSpace(root, rectangle):
    if(root.rect != None):
        return findSpace(root.right, rectangle)
    return None

def cutSpace():
    return None

def increaseSpace():
    return None

def getOriginalIndexKey(item):
    return item[2]

def getHeightKey(item):
    return item[1]



class Node:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.rect = val