import operator
from collections import deque
import itertools
class Packer:
    def __init__(self):
        self.Tree = None


def find_solution(rectangles, throttle):
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
    packed_tree = Tree(throttle)

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
    def __init__(self, throttle):
        self.root = None
        self.throttle = throttle
        empty_spaces.clear()

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
            if space.isEmpty and (rectangle[0] <= space.rectTuple[0]) and (rectangle[1] <= space.rectTuple[1]):
                # We do!
                best_fit = space
                # return space

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

        # if self.root.rectTuple[0] + rectangle[0] > self.root.rectTuple[1] + rectangle[1]:
        #     defGoDown = True
        # else:
        #     defGoRight = True

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

        # some_node = self.search_spaces(rectangle)
        # if some_node:
        #     some_node.splitSpace(rectangle)
        #     return some_node
        # else:
        #     return None
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

        # some_node = self.search_spaces(rectangle)
        # if some_node:
        #     some_node.splitSpace(rectangle)
        #     return some_node
        # else:
        #     return None
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
