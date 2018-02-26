from BaseAI_3 import BaseAI
from Grid_3 import Grid
from Heuristics import Heuristics
from Node import Node
from MiniMaxTree import MiniMax


class PlayerAI(BaseAI):

    def __init__(self):
        self.h = Heuristics()

    def getMove(self, grid):
        node1 = Node(grid, 0)
        strategy = MiniMax(node1)
        alpha_beta = strategy.alpha_beta(3)

        return alpha_beta

        # moves = grid.getAvailableMoves()
        # return moves[randint(0, len(moves) - 1)] if moves else None
