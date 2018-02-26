from Grid_3 import Grid
from Heuristics import Heuristics
from Node import Node


class MiniMax:
    def __init__(self, root_node, parameters):
        self.root = root_node
        self.h_eval = Heuristics(parameters)
        self.best_direction = None
        self.direction_list = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def alpha_beta(self, depth):
        result = self.alpha_beta_recursive(self.root, depth, -float('inf'), float('inf'), True)

        for child in self.root.children:
            if child.h_value == result:
                self.best_direction = child.direction
                return self.best_direction
                #print("Child h_value = ", child.h_value,"\nBest move =", self.best_direction)

        return result

    def alpha_beta_recursive(self, node, depth, a, b, MaxPlayer = True):
        if depth == 0:
            h_terminal = self.h_eval.evaluate_h(node.grid)
            node.h_value = h_terminal
            return h_terminal

        if MaxPlayer:
            available_moves = node.grid.getAvailableMoves()
            if len(available_moves) == 0:
                h_terminal = self.h_eval.evaluate_h(node.grid)
                node.h_value = h_terminal
                return h_terminal

            v = -float('inf')

            for direction in available_moves:
                new_grid = node.grid.clone()
                new_grid.move(direction)
                new_child = Node(new_grid, h_value=0, parent=node, direction=direction)
                node.push_children(new_child)

                v = max(v, self.alpha_beta_recursive(new_child, depth-1, a, b, False))
                a = max(a, v)
                node.h_value = v
                if a >= b:
                    break   # pruning

            return v
        else:

            available_moves = node.grid.getAvailableCells()
            if len(available_moves) == 0:
                h_terminal = self.h_eval.evaluate_h(node.grid)
                node.h_value = h_terminal
                return h_terminal

            v = float('inf')

            for xy in available_moves:
                for value in (2, 4):
                    # if value == 4: break  ####################
                    new_grid = node.grid.clone()
                    new_grid.setCellValue(xy, value)
                    new_child = Node(new_grid, h_value=0, parent=node, direction=None)
                    node.push_children(new_child)

                    v = min(v, self.alpha_beta_recursive(new_child, depth-1, a, b, True))
                    b = min(b, v)
                    node.h_value = v
                    if a >= b:
                        break   # pruning

            return v
