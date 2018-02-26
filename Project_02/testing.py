from random import randint
from BaseAI_3 import BaseAI
from Grid_3 import Grid
from Heuristics import Heuristics
from Node import Node
from SearchTree import SearchTree
# from MiniMax import MiniMax
from MiniMaxTree import MiniMax
import time


class PlayerAI(BaseAI):

    def __init__(self):
        self.h = Heuristics()

    def getMove(self, grid):

        moves = grid.getAvailableMoves()
        print("\nmoves: ",moves)
        print("h = ", self.h.monotonicity(grid))
        return moves[randint(0, len(moves) - 1)] if moves else None


def main1():

    matrix = []

    matrix.append([ [1,      1,      1,      1],
                    [1,      1,      1,      1],
                    [1,      1,      1,      1],
                    [1,      1,      1,      1]])  # [0] only 1's
    matrix.append([ [2,      2,      2,       2],
                    [2,      2,      2,       2],
                    [2,      2,      2,       2],
                    [2,      2,      2,       2]])  # [1] only 2's
    matrix.append([ [4,      2,      4,      2],
                    [4,      2,      4,      2],
                    [2,      4,      2,      4],
                    [4,      2,      2,      4]])  # [2] 2's and 4's
    matrix.append([ [512,      64,      32,      8],
                    [256,      16,      8,      4],
                    [32,      8,      4,      0],
                    [8,      0,      0,      0]])  # [3] "perfect" monotonic matrix with high values
    matrix.append([ [8,      32,      64,      512],
                    [4,      8,      16,      256],
                    [0,      4,      8,      32],
                    [0,      0,      0,      8]])  # [4] horizontally flipped "perfect" monotonic matrix
    matrix.append([[32, 16, 4, 2],
                   [16, 8,  4, 2],
                   [4,  4,  4, 2],
                   [2,  2,  2, 2]])  # [5] "perfect" monotonic with low values and full
    matrix.append([[32, 16,  4, 2],
                   [16,  8,  4, 2],
                   [0,   0,  0, 0],
                   [0,   0,  0, 0]])  # [6] "perfect" monotonic with low values and NOT FULL
    matrix.append([[32, 16, 2, 4],
                   [2, 8, 0, 2],
                   [0, 4, 0, 0],
                   [0, 0, 0, 2]])  # [7] ALMOST "perfect" monotonic with low values and NOT FULL
    matrix.append([ [1,      1,      1,      1],
                    [1,      1,      1,      1],
                    [1,      1,      1,      1],
                    [1,      1,      1,      1]])
    matrix.append([[2, 2, 2, 2],
                   [0, 2, 2, 2],
                   [0, 0, 2, 2],
                   [0, 0, 0, 2]])


    h = Heuristics()

    print("Monotonicity\t\tEmptiness\t\tAdj Diff")
    for index, m in enumerate(matrix):
        grid = lambda: None
        grid.map = m
        grid.size = 4
        print("hm[", index, "]= {0:.3f}~".format(h.monotonicity(grid)),
              "\tempty =", h.empty_tiles(grid),
              "\t\tdiff ={0:.3f}".format(h.adj_difference(grid)))


    print("\nTotal Heuristics\t\tSame - adj_diff")

    for index, m in enumerate(matrix):
        grid = lambda: None
        grid.map = m
        grid.size = 4
        print("h[", index, "]= {0:.3f}".format(h.evaluate_h(grid, False)),
              "  \t\th[", index, "]= {0:.3f}".format(h.evaluate_h(grid, True)))

def main2():
    # my_node = Node(Grid(),0)
    # my_node.grid.setCellValue((3,3), 1)
    # my_node.print_grid()

    grid1 = Grid()
    grid1.setCellValue((0, 0), 1)
    grid2 = grid1.clone()
    grid2.setCellValue((0, 1), 1)   # child of node1
    grid3 = grid1.clone()
    grid3.setCellValue((0, 1), 2)   # child of node1
    grid4 = grid2.clone()
    grid4.setCellValue((0, 2), 1)   # child of node2
    grid5 = grid3.clone()
    grid5.setCellValue((0, 2), 1)  # child of node3

    node1 = Node(grid1, 0)
    node2 = Node(grid2, 0)
    node3 = Node(grid3, 0)
    node4 = Node(grid4, 0)
    node5 = Node(grid5, 0)

    node1.push_children(node2)
    node1.push_children(node3)
    node2.push_children(node4)
    node3.push_children(node5)

    my_tree = SearchTree(node1)

    my_tree.print_tree()

def main3():
    grid1 = Grid()
    node1 = Node(grid1, 0)
    grid1.map[0][0] = 2
    grid1.map[1][0] = 2
    grid1.map[3][0] = 4

    grid1.map[0][1] = 0
    grid1.map[1][1] = 0
    grid1.map[3][1] = 0
    grid1.map[2][1] = 0
    grid1.map[2][2] = 0

    my_tree = SearchTree(node1)
    my_tree.build_tree(4)
    my_tree.print_tree()

    strategy = MiniMax(node1)
    alpha_beta = strategy.alpha_beta(4)

    print("\nMiniMax: {0:.4f}".format(alpha_beta))

    print("---------> ", node1.h_value)

def main4():
    grid1 = Grid()
    node1 = Node(grid1, 0)
    grid1.map[0][0] = 64
    grid1.map[1][0] = 2
    grid1.map[3][0] = 4

    grid1.map[0][1] = 0
    grid1.map[1][1] = 0
    grid1.map[3][1] = 0
    grid1.map[2][1] = 0
    grid1.map[2][2] = 0

    my_tree = SearchTree(node1)
    my_tree.build_tree(4)

    strategy = MiniMax(node1)
    alpha_beta = strategy.alpha_beta(5)

    print("\nMiniMax: ", node1.h_value, "\nDirection: ", alpha_beta)

def main():
    grid1 = Grid()
    node1 = Node(grid1, 0)
    grid1.map[0][0] = 64
    grid1.map[1][0] = 2
    grid1.map[3][0] = 4

    grid1.map[0][1] = 0
    grid1.map[1][1] = 0
    grid1.map[3][1] = 0
    grid1.map[2][1] = 0
    grid1.map[2][2] = 0

    strategy = MiniMax(node1)
    alpha_beta = strategy.alpha_beta(5)

    print("\nMiniMax: ", node1.h_value, "\nDirection: ", alpha_beta)
    #time.sleep(999999)

if __name__ == '__main__':
    main()