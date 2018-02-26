from Grid_3 import Grid
from Heuristics import Heuristics
from Node import Node

class MiniMax:
    def __init__(self, root_node):
        self.root = root_node
        self.h_eval = Heuristics()
        self.best_direction = None
        self.direction_list = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def alpha_beta(self, depth):
        result = self.alpha_beta_recursive(self.root, depth, -float('inf'), float('inf'), True)

        for child in self.root.children:
            if child.h_value == result:
                self.best_direction = self.direction_list[child.direction]
                print("Child h_value = ", child.h_value,"\nBest move =", self.best_direction)

        return result

    def alpha_beta_recursive(self, node, depth, a, b, MaxPlayer = True):
        if depth == 0 or len(node.children) == 0:
            h_terminal = self.h_eval.evaluate_h(node.grid)
            node.h_value = h_terminal
            return h_terminal
        if MaxPlayer:
            for child in node.children:
                a = max(a, self.alpha_beta_recursive(child, depth-1, a, b, False))
                node.h_value = max(node.h_value, child.h_value)
                if a >= b:
                    break   # pruning

            return a
        else:
            for child in node.children:
                b = min(b, self.alpha_beta_recursive(child, depth-1, a, b, True))
                node.h_value = min(node.h_value, child.h_value)
                if a >= b:
                    break   # pruning

            return b
