from BaseAI_3 import BaseAI
from Grid_3 import Grid


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


class Heuristics:

    def __init__(self):
        #self.monotonicity_weights = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.monotonicity_weights_1 = (1073741824, 268435456, 67108864, 16777216, 4194304, 1048576, 262144, 65536, 16384, 4096, 1024, 256, 64, 16, 4, 1)
        self.monotonicity_weights_2 = (1073741824, 268435456, 67108864, 16777216, 65536, 262144, 1048576, 4194304, 16384, 4096, 1024, 256, 1, 4, 16, 64)
        self.monotonicity_weights_3 = (16777216, 67108864, 268435456, 1073741824, 4194304, 1048576, 262144, 65536, 256, 1024, 4096, 16384, 64, 16, 4, 1)
        self.monotonicity_weights_4 = (1, 4, 16, 64, 16384, 4096, 1024, 256, 65536, 262144, 1048576, 4194304, 1073741824, 268435456, 67108864, 16777216)
        self.monotonicity_weights_5 = (64, 16, 4, 1, 256, 1024, 4096, 16384, 4194304, 1048576, 262144, 65536, 16777216, 67108864, 268435456, 1073741824)


        self.monotonicity_sum_weights = 1431655765/4  # 357913941.25  #/4


    # def monotonicity_new(self, grid):
    #     return max(sum(self.monotonicity_weights_2[grid.size*i + j]*grid.map[i][j]
    #                for i in range(grid.size) for j in range(grid.size))/self.monotonicity_sum_weights,
    #                sum(self.monotonicity_weights_3[grid.size * i + j] * grid.map[i][j]
    #                    for i in range(grid.size) for j in range(grid.size)) / self.monotonicity_sum_weights,
    #                sum(self.monotonicity_weights_4[grid.size * i + j] * grid.map[i][j]
    #                    for i in range(grid.size) for j in range(grid.size)) / self.monotonicity_sum_weights,
    #                sum(self.monotonicity_weights_5[grid.size * i + j] * grid.map[i][j]
    #                    for i in range(grid.size) for j in range(grid.size)) / self.monotonicity_sum_weights
    #                )

    def monotonicity(self, grid):
        return sum(self.monotonicity_weights_2[grid.size*i + j]*grid.map[i][j]
                   for i in range(grid.size) for j in range(grid.size))/self.monotonicity_sum_weights

    def uniqueness(self, grid):
        my_set = set()
        zeros = 0

        for i in range(grid.size):
            for j in range(grid.size):
                if grid.map[i][j] != 0:
                    my_set.add(grid.map[i][j])
                else:
                    zeros += 1

        return (len(my_set)+zeros)

    # def repetition(self, grid):
    #     my_set = set()
    #     my_list = []
    #     repetition = 0
    #
    #     for i in range(grid.size):
    #         for j in range(grid.size):
    #             element = grid.map[i][j]
    #             if element != 0:
    #                 my_set.add(element)
    #                 my_list.append(element)
    #
    #         for number in my_set:
    #             freq = my_list.count(number)
    #             if freq > 1:
    #                 repetition += freq
    #
    #     return repetition

    @staticmethod
    def empty_tiles(grid):
        count = 0
        for r in range(grid.size):
            for c in range(grid.size):
                if grid.map[r][c] == 0:
                    count +=1
        return count

    @staticmethod
    def adj_difference(grid):
        diff = 0
        max_tile = 0
        size = grid.size

        for r in range(size):
            for c in range(size):
                tile = grid.map[r][c]
                max_tile = max(max_tile, tile)

                if r%2 == c%2:  # if row and column are both even or both odd
                    if r-1 >= 0:     diff += abs(tile - grid.map[r-1][c])
                    if r+1 < size:  diff += abs(tile - grid.map[r+1][c])
                    if c-1 >= 0:     diff += abs(tile - grid.map[r][c-1])
                    if c+1 < size:  diff += abs(tile - grid.map[r][c+1])
                    #print("diff [",r,"][",c,"] = ",diff2)

        return diff/max_tile

    def evaluate_h(self, grid, diff = True):

        if diff:
            #h = self.monotonicity(grid) * (1 + self.empty_tiles(grid)/8)
            #h = self.monotonicity(grid) * (1 + (self.empty_tiles(grid) - self.adj_difference(grid)) / 16)
            #h = 512 + self.monotonicity(grid) * (1 + self.empty_tiles(grid)/16) - self.adj_difference(grid)
            #h = 512 + self.monotonicity(grid) + self.empty_tiles(grid) - self.adj_difference(grid)
            #h = 1024 + self.monotonicity(grid) + self.empty_tiles(grid) - 4*self.adj_difference(grid)
            # h = 1024 + self.monotonicity(grid) - 2 * self.adj_difference(grid) + 4*self.uniqueness(grid)
            # h = 1024 + self.monotonicity(grid) - 2 * self.adj_difference(grid) + 4*self.uniqueness(grid)
            h = 1024 + self.monotonicity(grid) - 2 * self.adj_difference(grid) + 4 * self.uniqueness(grid)
        else:
            pass
            # h = self.monotonicity(grid) * (1 + self.empty_tiles(grid)/grid.size**2)

        return h if h > 0 else 0


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
                    if value == 4: break  ####################
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