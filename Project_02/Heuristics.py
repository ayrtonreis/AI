from Grid_3 import Grid

class Heuristics:

    def __init__(self):
        #self.monotonicity_weights = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.monotonicity_weights_1 = (1073741824, 268435456, 67108864, 16777216, 4194304, 1048576, 262144, 65536, 16384, 4096, 1024, 256, 64, 16, 4, 1)
        self.monotonicity_weights_2 = (1073741824, 268435456, 67108864, 16777216, 65536, 262144, 1048576, 4194304, 16384, 4096, 1024, 256, 1, 4, 16, 64)
        self.monotonicity_weights_3 = (16777216, 67108864, 268435456, 1073741824, 4194304, 1048576, 262144, 65536, 256, 1024, 4096, 16384, 64, 16, 4, 1)
        self.monotonicity_weights_4 = (1, 4, 16, 64, 16384, 4096, 1024, 256, 65536, 262144, 1048576, 4194304, 1073741824, 268435456, 67108864, 16777216)
        self.monotonicity_weights_5 = (64, 16, 4, 1, 256, 1024, 4096, 16384, 4194304, 1048576, 262144, 65536, 16777216, 67108864, 268435456, 1073741824)


        self.monotonicity_sum_weights = 357913941.25  # 1431655765/4  #/4


    def monotonicity_new(self, grid):
        return max(sum(self.monotonicity_weights_2[grid.size*i + j]*grid.map[i][j]
                   for i in range(grid.size) for j in range(grid.size))/self.monotonicity_sum_weights,
                   sum(self.monotonicity_weights_3[grid.size * i + j] * grid.map[i][j]
                       for i in range(grid.size) for j in range(grid.size)) / self.monotonicity_sum_weights,
                   sum(self.monotonicity_weights_4[grid.size * i + j] * grid.map[i][j]
                       for i in range(grid.size) for j in range(grid.size)) / self.monotonicity_sum_weights,
                   sum(self.monotonicity_weights_5[grid.size * i + j] * grid.map[i][j]
                       for i in range(grid.size) for j in range(grid.size)) / self.monotonicity_sum_weights
                   )

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

