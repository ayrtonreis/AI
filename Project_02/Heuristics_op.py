from Grid_3 import Grid

class Heuristics:

    def __init__(self, parameters):
        #self.monotonicity_weights = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.monotonicity_weights = (1073741824, 268435456, 67108864, 16777216, 4194304, 1048576, 262144, 65536, 16384, 4096, 1024, 256, 64, 16, 4, 1)
        self.monotonicity_sum_weights = 1431655765
        self.c = parameters


    def monotonicity(self, grid):
        return sum(self.monotonicity_weights[grid.size*i + j]*grid.map[i][j]
                   for i in range(grid.size) for j in range(grid.size))/self.monotonicity_sum_weights

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
            h = self.monotonicity(grid) * (self.c[0] + self.empty_tiles(grid)/self.c[1] - self.adj_difference(grid)/self.c[2])
        else:
            h = self.monotonicity(grid) * (1 + self.empty_tiles(grid)/grid.size**2)

        return h if h > 0 else 0

