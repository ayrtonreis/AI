from Grid_3 import Grid

class Node:

    def __init__(self, grid, h_value=None, parent=None, direction=None):
        self.parent = parent
        self.grid = grid
        self.h_value = h_value
        self.direction = direction
        self.children = []

    def push_children(self, child):
        self.children.append(child)

    def print_grid(self):
        for i in self.grid.map:
            print(i)
        print("\t\t\th = {0:.4f}".format(self.h_value))