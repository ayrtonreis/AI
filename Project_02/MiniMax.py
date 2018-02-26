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
                self.best_direction = child.direction
                return self.best_direction

        return result

    def alpha_beta_recursive(self, node, depth, a, b, MaxPlayer = True):
        if depth == 0 or len(node.children) == 0:
            h_terminal = self.h_eval.evaluate_h(node.grid)
            node.h_value = h_terminal
            return h_terminal
        if MaxPlayer:
            v = -float('inf')
            for child in node.children:
                v = max(v, self.alpha_beta_recursive(child, depth-1, a, b, False))
                a = max(a, v)
                node.h_value = v
                if a >= b:
                    break   # pruning

            return v
        else:
            v = float('inf')
            for child in node.children:
                v = min(v, self.alpha_beta_recursive(child, depth-1, a, b, True))
                b = min(b, v)
                node.h_value = v
                if a >= b:
                    break   # pruning

            return v
