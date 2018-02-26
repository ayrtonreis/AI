from Grid_3 import Grid
from Heuristics import Heuristics
from Node import Node

class SearchTree:

    def __init__(self, root_node):
        self.root = root_node
        self.count = 0
        self.heuristic = Heuristics()

    def build_tree(self, depth=1):
        self.build_recursive(depth, self.root)

    def print_tree(self):
        print("\n----PRINTING THE SEARCH TREE----")
        self.print_recursive(self.root)
        print("Num of nodes: ", self.count)

    def print_recursive(self, node):
        self.count +=1
        print("direction: ", node.direction)
        node.print_grid()
        if len(node.children) == 0:
            print("LEAF above\n___________")
            return

        for child in node.children:
            self.print_recursive(child)

    def build_recursive(self, depth, node, player_turn=True):
        if depth == 0:  # Base case
            node.h_value = self.heuristic.evaluate_h(node.grid, diff=True)
            return

        if player_turn:
            available_moves = node.grid.getAvailableMoves()
            if len(available_moves) == 0:
                return
            for direction in available_moves:
                new_grid = node.grid.clone()
                new_grid.move(direction)
                new_child = Node(new_grid, h_value=0, parent=node,direction=direction)
                node.push_children(new_child)
                self.build_recursive(depth-1, new_child, False)
        else:  # computer's turn
            available_moves = node.grid.getAvailableCells()
            if len(available_moves) == 0:
                return
            for xy in available_moves:
                for value in (2, 4):
                    #if value == 4: break  ####################
                    new_grid = node.grid.clone()
                    new_grid.setCellValue(xy, value)
                    new_child = Node(new_grid, h_value=0, parent=node, direction=None)
                    node.push_children(new_child)
                    self.build_recursive(depth-1, new_child, True)