from Solver import Solver

def main_1():
    #initial_state = (6, 4, 1, 8, 3, 5, 0, 2, 7)
    #initial_state = (8, 6, 7, 2, 5, 4, 3, 0, 1)  # hard
    initial_state = (1,0,2,3,4,5,6,7,8)

    solver = Solver(initial_state, "ida")
    solver.run()
    solver.create_output()
    print_file("output.txt")

    solver = Solver(initial_state, "ast")
    solver.run()
    solver.create_output()
    print_file("output.txt")


    solver = Solver(initial_state, "bfs")
    solver.run()
    solver.create_output()
    print_file("output.txt")

    solver = Solver(initial_state, "dfs")
    solver.run()
    solver.create_output()
    print_file("output.txt")

def main():
    # initial_state = (4, 2, 3, 6, 5, 9, 12, 7, 1, 13, 11, 15, 8, 10, 14, 0)
    initial_state = (9, 6, 5, 2, 1, 4, 7, 3, 8, 12, 0, 11, 14, 13, 10, 15)

    solver = Solver(initial_state, "ida")
    solver.run()
    solver.create_output()
    print_file("output.txt")

    solver = Solver(initial_state, "ast")
    solver.run()
    solver.create_output()
    print_file("output.txt")

def print_file(file_name):
    f = open(file_name, 'r')
    message = f.read()
    print(file_name, message, '', sep='\n---------------------------------------\n')
    f.close()


if __name__ == '__main__':
    main()