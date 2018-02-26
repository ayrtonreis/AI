import copy
def create_global_var():
    ROWS = []
    COLS = []
    BOXES = []

    for char in rows:
         ROWS.append(cross(char,digits))

    for digit in digits:
         COLS.append(cross(rows,digit))

    row_blocks = ["ABC", "DEF", "GHI"]
    col_blocks = ["123", "456", "789"]

    for rb in row_blocks:
        for cb in col_blocks:
            BOXES.append(cross(rb, cb))

    # returns tiles, ROWS, COLS
    return cross(rows, cols), ROWS, COLS, BOXES

def cross(A, B):
    return [a+b for a in A for b in B]

def to_string(grid):
    return ''.join(grid.values())

def compare_strings(result, answer):
    print("_______________")
    if len(result) != 81:
        print("LENGTH ERROR: ", len(result))
    elif result == answer:
        print("SUCCESS! EQUAL STRINGS!")
    else:
        print("SAME LENGTH, BUT DIFFERENT!")
    print("_______________")

def generate_constraints():
    constraints = set()

    my_list = cross(rows, digits)
    for position in my_list:
        neighbors = get_neighbors(position)
        while len(neighbors) > 0:
            n = neighbors.pop()
            constraints.add((position, n))

    return constraints

def to_grid(grid_string):
    values = dict((key, digits) for key in tiles)

    for key, digit in zip(values, grid_string):
        if digit in digits:
            values[key] = digit

    return values

def get_neighbors(position):
    neighbors = set()

    for row in ROWS:
        if position in row:
            neighbors.update(row)
            break

    for col in COLS:
        if position in col:
            neighbors.update(col)
            break

    for box in BOXES:
        if position in box:
            neighbors.update(box)
            break
    neighbors.discard(position)

    return neighbors

def solve(str_in):
    grid = to_grid(str_in)
    ac3(grid)
    print(grid)
    if len(to_string(grid)) != 81:
        return backtracking(grid)

    #return to_string(grid)
    return grid

def ac3(formated_grid):
    constraints = generate_constraints()

    while len(constraints) > 0:
        pair = constraints.pop()
        Xi = pair[0]
        Xj = pair[1]

        if remove_inconsistent_values(Xi,Xj, formated_grid):
            for Xk in get_neighbors(Xi):
                constraints.add((Xk, Xi))


def remove_inconsistent_values(Xi, Xj, grid):
    removed = False
    for x in grid[Xi]:
        satisfied = False
        for y in grid[Xj]:
            if x != y:
                satisfied = True
                break
        if not satisfied:
            # print("Xi at", Xi, " - ", grid[Xi])
            # print("Xj at", Xj, " - ", grid[Xj])
            # print("NOT SATISFIED! ", x, " in ", grid[Xi])
            grid[Xi] = grid[Xi].replace(x, "")
            #print(grid[Xi])
            removed = True


    return removed

def backtracking(grid):
    return recursive_backtracking(grid)

def recursive_backtracking(grid):
    if len(to_string(grid)) == 81:
        return grid # SUCCESS! FINISHED!
    position = select_unnasigned(grid)
    values = copy.deepcopy(grid[position])

    for v in values:
        if is_consistent(grid, position, v):
            grid[position] = v
            result = recursive_backtracking(grid)
            if result is not False:
                return result
            else:
                grid[position] = values

    return False

def select_unnasigned(grid):
    min_options = 10 # (max number of options = 9) + 1
    position = 'A1' # random initial position

    for key in tiles:
        size = len(grid[key])
        if size > 1 and size < min_options:
            min_options = size
            position = key

    return position

def is_consistent(grid, position, value):
    neighbors_keys = get_neighbors(position)

    for key in neighbors_keys:
        if value == grid[key]:
            return False

    return True

# Global Variables
digits = "123456789"
rows = "ABCDEFGHI"
cols = digits
tiles, ROWS, COLS, BOXES = create_global_var()

def main1():
    #str_in = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
    #str_out = "483921657967345821251876493548132976729564138136798245372689514814253769695417382"

    str_in = "094000130000000000000076002080010000032000000000200060000050400000008007006304008"
    str_out = "794582136268931745315476982689715324432869571157243869821657493943128657576394218"

    my_grid = to_grid(str_in)

    print("BEFORE: ")
    print(my_grid.values())
    ac3(my_grid)
    print("AFTER:")
    print(my_grid.values())
    print(to_string(my_grid))
    compare_strings(to_string(my_grid), str_out)
    print("\n\n")

    A = "AB"
    B = "123"
    print(cross(A,B))
    print("rows:\n", ROWS)
    print("cols:\n", COLS)
    print("boxes:\n", BOXES)
    print("neighbors: ", get_neighbors('A1'))
    print("constraints: ", len(generate_constraints()))

def main2():

    str_in =  "000000000000942080160000029000000008906000001400250000004000000020008090050000700"
    str_out = "249186573735942186168375429512697348976834251483251967694723815327518694851469732"

    result = solve(str_in)
    print(len(to_string(result)))
    print(compare_strings(to_string(result), str_out))
    print(to_string(result))
    print(result)

def main():

    str_in =  "000000000000942080160000029000000008906000001400250000004000000020008090050000700"
    str_out = "249186573735942186168375429512697348976834251483251967694723815327518694851469732"

    result = solve(str_in)
    print(len(to_string(result)))
    compare_strings(to_string(result), str_out)
    print(to_string(result))
    print(result)

def main3():

    str_in =  "000000000000942080160000029000000008906000001400250000004000000020008090050000700"
    str_out = "249186573735942186168375429512697348976834251483251967694723815327518694851469732"

    print(len(generate_constraints()))

if __name__ == '__main__':
    main()