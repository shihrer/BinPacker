from collections import deque


class Packer:
    def __init__(self):
        self.root = None
        self.recursive = False
        self.best_fit = True
        # IDEA: keep nodes sorted by smallest, then first found fit will be best.
        # This list grows a lot if max size is increased...  Why?
        self.empty_nodes = deque()

    def pack(self, rectangles):
        blocks = []

        for rectangle in rectangles:
            if self.root is None:
                self.root = Node((0, 0), rectangles[0])
                some_node = self.root
                self.empty_nodes.append(self.root)
            else:
                some_node = self.find_node(rectangle)

            if some_node is not None:
                blocks.append(self.split_node(some_node, rectangle))
            else:
                blocks.append(self.grow_node(rectangle))

        return blocks

    def find_node(self, size):
        if self.recursive:
            return self.find_node_r(self.root, size)
        else:
            best_node = None

            for node in self.empty_nodes:
                if node.check_fit(size) is True:
                    if not self.best_fit:
                        return node

                    if best_node:
                        if node.better_fit(best_node, size):
                            best_node = node
                    else:
                        best_node = node

            return best_node

    def find_node_r(self, some_node, size):
        if some_node:
            if some_node.used:
                return self.find_node_r(some_node.right, size) or self.find_node_r(some_node.down, size)
            elif some_node.fits(size):
                return some_node

        return None

    def split_node(self, some_node, size):
        some_node.used = True
        self.empty_nodes.remove(some_node)

        # Check to see if there's space to even split
        if some_node.size[1] - size[1] > 0:
            some_node.down = Node((some_node.location[0], some_node.location[1] + size[1]),
                                  (some_node.size[0], some_node.size[1] - size[1]))

            self.empty_nodes.appendleft(some_node.down)

        if some_node.size[0] - size[0] > 0:
            some_node.right = Node((some_node.location[0] + size[0], some_node.location[1]),
                                   (some_node.size[0] - size[0], size[1]))

            self.empty_nodes.appendleft(some_node.right)

        some_node.size = size
        return Block(some_node.location, size)

    def grow_node(self, size):
        # Needs to handle really wide blocks better
        can_go_down = size[0] <= self.root.size[0]      # check if rectangle width is less than root
        can_go_right = size[1] <= self.root.size[1]     # check if rectangle height is less than root

        should_go_down = can_go_down and (self.root.size[0] >= (self.root.size[1] + size[1]))
        should_go_right = can_go_right and (self.root.size[1] >= (self.root.size[0] + size[0]))

        if should_go_right:
            return self.grow_right(size)
        elif should_go_down:
            return self.grow_down(size)
        elif can_go_right:
            return self.grow_right(size)
        elif can_go_down:
            return self.grow_down(size)

        return None

    def grow_right(self, size):
        new_root = Node((0, 0), (self.root.size[0] + size[0], self.root.size[1]))
        new_root.used = True
        new_root.down = self.root
        new_root.right = Node((self.root.size[0], 0),
                              (size[0], self.root.size[1]))

        self.root = new_root

        if self.root.right.size[0] > 0 and self.root.right.size[1] > 0:
            self.empty_nodes.appendleft(self.root.right)

        return self.split_node(self.root.right, size)

    def grow_down(self, size):
        new_root = Node((0, 0), (self.root.size[0], self.root.size[1] + size[1]))
        new_root.used = True
        new_root.right = self.root
        new_root.down = Node((0, self.root.size[1]),
                             (self.root.size[0], size[1]))

        self.root = new_root

        if self.root.down.size[0] > 0 and self.root.down.size[1] > 0:
            self.empty_nodes.appendleft(self.root.down)

        return self.split_node(self.root.down, size)


class Node:
    def __init__(self, location, size):
        self.used = False
        self.down = None
        self.right = None
        self.location = location
        self.size = size

    def fits(self, size):
        return size[1] <= self.size[1] and size[0] <= self.size[0]

    def check_fit(self, size):
        return size[1] <= self.size[1] and size[0] <= self.size[0]

    def better_fit(self, some_node, size):
        return self.size[0] - size[0] < some_node.size[0] - size[0] or self.size[1] - size[1] < some_node.size[1] - size[1]


class Block:
    def __init__(self, location, size):
        self.size = size
        self.location = location
        self.rect = location + size
