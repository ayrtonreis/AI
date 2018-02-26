import sys
import resource
import math
import time
from collections import deque
from heapq import heappush, heappop

MAX_INT = sys.maxsize


class Solver:
    def __init__(self, initial_state, method):
        self.initial_state = initial_state
        self.method = method.lower()

        self.goal_state = tuple(range(len(initial_state)))
        self.start_time = time.clock()
        self.stop_time = self.start_time
        self.expanded = 0
        self.fringe_order = 0
        self.fringe_size = 1
        self.max_fringe_size = 1
        self.max_search_depth = 0
        self.path_to_goal = []
        self.fringe = None
        self.last_node = None

        #print('GOAL STATE: ', self.goal_state, "    -    ", self.method.upper())


    def create_output(self):
        '''back_track = self.last_node

        while back_track.parent != None:
            back_track.print()
            #print("  D = ", back_track.depth, "   TC = ", back_track.total_cost, "   h= ", back_track.total_cost- back_track.depth)
            back_track = back_track.parent'''

        self.handle_output(path=self.path_to_goal, cost=self.last_node.total_cost, expanded=self.expanded, fringe_size=self.fringe_size, max_fringe_size=self.max_fringe_size,depth=self.last_node.depth, max_depth=self.max_search_depth, running_time=self.stop_time, ram=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

    def handle_output(self,path=[], cost='*', expanded='*', fringe_size='*', max_fringe_size='*', depth='*', max_depth='*', running_time='*', ram='*'):
        file = open("output.txt", "w")
        if self.expanded == 0:
            file.write("path_to_goal: []\n")
        else:
            file.write("path_to_goal: [\'" + '\', \''.join(path) + "\']\n")
        file.write("cost_of_path: " + '{}'.format(int(cost)) + "\n")
        file.write("nodes_expanded: " + '{}'.format(expanded) + "\n")
        file.write("fringe_size: " + '{}'.format(fringe_size) + "\n")
        file.write("max_fringe_size: " + '{}'.format(max_fringe_size) + "\n")
        file.write("search_depth: " + '{}'.format(depth) + "\n")

        if self.method == "dfs" and max_depth > 1:
            max_depth -= 1
        file.write("max_search_depth: " + '{}'.format(max_depth) + "\n")

        file.write("running_time: " + '{0:.8f}'.format(running_time) + "\n")
        file.write("max_ram_usage: " + '{0:.8f}'.format(ram))
        file.close()


    def initialize_fringe(self):
        root_node = Node(data=self.initial_state)

        if self.method == "bfs":
            self.fringe = deque()
            self.fringe.appendleft(root_node)
        elif self.method == "dfs":
            self.fringe = deque()
            self.fringe.append(root_node)
        elif self.method == "ida":
            self.fringe = deque()
            self.fringe.append(root_node)
        elif self.method == "ast":
            self.fringe = []
            heappush(self.fringe,(0, self.fringe_order, root_node))  # the priority queue gets a tuple of the form (priority, Node)

    def pop_fringe(self):
        if self.method == "bfs" or self.method == "dfs":
            node = self.fringe.pop()
            return node
        elif self.method == "ida":
            node = self.fringe.pop()
            return node
        elif self.method == "ast":
            #print("\nFringe: ")
            #for element in self.fringe:
                #print("Cost:", element[0], " ", element[2].data, "-")
            t = heappop(self.fringe)
            #print("Chosen: ", t[2].data)
            return t[2]  # returns only the Node from the tuple of the form (priority, Node)

    def fringe_append(self,child):
        if self.method == "bfs":
            self.fringe.appendleft(child)
        elif self.method == "dfs":
            self.fringe.append(child)
        elif self.method == "ida":
            self.fringe.append(child)
        elif self.method == "ast":
            heappush(self.fringe, (child.total_cost, self.fringe_order, child))
        self.fringe_order += 1

    def expand_node(self, node):
        my_list = node.expand()
        if self.method == "dfs" or self.method == "ida":
            my_list.reverse()
            return my_list
        else:
            return my_list

    def run(self):
        if self.method == "ida":
            self.run_ida()
        else:
            self.run_generic()

    def run_generic(self, cutoff=MAX_INT):
        self.initialize_fringe()
        self.fringe_size = 1
        history = set()

        if self.method == "ida":
            history.add(self.initial_state)  # create a set of tuples of the form (<tuple>node.data, <int>node.depth)
        else:
            history.add(self.initial_state)  # create a set with the tuples which are or were in the fringe

        while self.fringe_size > 0:  # checks if fringe IS NOT empty
            node = self.pop_fringe()
            self.fringe_size -= 1

            if node.data == self.goal_state:
                self.stop_time = time.clock() - self.start_time
                self.last_node = node
                back_track = node

                while back_track.parent != None:
                    self.path_to_goal.append(back_track.origin)
                    back_track = back_track.parent

                self.path_to_goal.reverse()

                return True  # success

            elif node.depth < cutoff:
                #if self.expanded % 10000 == 0:
                    #print("->", self.expanded, "\n")

                successors = self.expand_node(node)
                self.expanded += 1

                search_depth = node.depth + 1

                if search_depth > self.max_search_depth:
                    self.max_search_depth = search_depth

                # print("HISTORY: ", end="")
                # print(history)

                for child in successors:
                    if self.method == "ida":
                        check_element = (child.data, child.depth)
                    else:
                        check_element = child.data

                    if not (check_element in history):  # if the state of the child is not in the history, then add it to the fringe
                        self.fringe_append(child)
                        history.add(check_element)

                        self.fringe_size += 1
                        if self.fringe_size > self.max_fringe_size:
                            self.max_fringe_size = self.fringe_size

                        #child.print()
                        #print(",   D = ", child.depth, "   TC = ", child.total_cost, "   h= ", child.total_cost- child.depth)
        return False  # fringe is empty

    def run_ida(self):  # ERROR: NOT TRYING EVERY POSSIBILITY IN EACH DEPTH
        cutoff = Node(self.initial_state).total_cost
        while True:
            result = self.run_generic_ida(cutoff=cutoff)
            if result == True:  # == True IS NOT REDUDANT in this case. It could be an integer
                return True  # success
            cutoff = result
            #print("Cutoff: ", cutoff)

    def run_generic_ida(self, cutoff=MAX_INT):
        self.expanded = 0  # re-count for ida for each iteration?
        self.initialize_fringe()
        self.fringe_size = 1
        history = set()
        min_for_ida = MAX_INT

        if self.method == "ida":
            history.add(self.initial_state)  # create a set of tuples of the form (<tuple>node.data, <int>node.depth)
        else:
            history.add(self.initial_state)  # create a set with the tuples which are or were in the fringe

        compared = 1

        while self.fringe_size > 0:  # checks if fringe IS NOT empty
            node = self.pop_fringe()
            self.fringe_size -= 1

            if self.method == "ida":
                compared = node.total_cost

            if node.data == self.goal_state:
                self.stop_time = time.clock() - self.start_time
                self.last_node = node
                back_track = node

                while back_track.parent != None:
                    self.path_to_goal.append(back_track.origin)
                    back_track = back_track.parent

                self.path_to_goal.reverse()

                return True  # success

            elif compared <= cutoff:
                #if self.expanded % 10000 == 0:
                    #print("->", self.expanded, "\n")

                successors = self.expand_node(node)
                self.expanded += 1

                search_depth = node.depth + 1

                if search_depth > self.max_search_depth:
                    self.max_search_depth = search_depth

                # print("HISTORY: ", end="")
                # print(history)

                for child in successors:
                    if self.method == "ida":
                        check_element = (child.data, child.depth)
                    else:
                        check_element = child.data

                    if not (check_element in history):  # if the state of the child is not in the history, then add it to the fringe
                        self.fringe_append(child)
                        history.add(check_element)

                        self.fringe_size += 1
                        if self.fringe_size > self.max_fringe_size:
                            self.max_fringe_size = self.fringe_size

                        #child.print()
                        #print(",   D = ", child.depth, "   TC = ", child.total_cost, "   h= ", child.total_cost- child.depth)
            else:  # node.total_cost > cutoff
                if compared < min_for_ida:
                    min_for_ida = compared

        # fringe is empty
        if self.method == "ida":
            return min_for_ida
        else:
            return False

    '''def run_ida(self):  # ERROR: NOT TRYING EVERY POSSIBILITY IN EACH DEPTH
        cutoff = 1
        while True:
            if self.run_generic(cutoff=cutoff):
                return True  # success
            cutoff += 1
            print("Cutoff: ", cutoff)'''


class Node:

    def __init__(self, data=None, parent=None, origin=None, heuristics=True, depth=0):
        self.data = data
        self.parent = parent
        self.origin = origin
        self.depth = depth

        self.n = int(math.sqrt(len(self.data)))
        self.index = self.data.index(0)
        self.row = int(self.index / self.n)
        self.col = int(self.index % self.n)

        self.total_cost = depth
        if heuristics:
            self.total_cost += self.manhattan_distance()

    def manhattan_distance(self):
        total_distance = 0
        for index, element in enumerate(self.data):
            if element != 0 and index != element:  # the empty spot is not considered
                diff = abs(index - element)  # current linear index - correct linear index (the latter is the number itself)
                total_distance += int(diff/self.n) + int(diff % self.n)
        return total_distance*0.9999
        # return total_distance * 0.99999999999999

    def expand(self):

        children = []

        for i in range(4):
            new_node = self.successor(i)

            if new_node is not False:
                children.append(new_node)

        return children

    def successor(self, operator):
        new_state = []
        movement = None

        if operator == 0 and self.row > 0:
            new_state = self.move(int(self.n*(self.row - 1) + self.col))
            movement = "Up"
        elif operator == 1 and self.row < self.n - 1:
            new_state = self.move(int(self.n*(self.row +1) + self.col))
            movement = "Down"
        elif operator == 2 and self.col > 0:
            new_state = self.move(int(self.n*self.row + self.col - 1))
            movement = "Left"
        elif operator == 3 and self.col < self.n - 1:
            new_state = self.move(int(self.n*self.row + self.col + 1))
            movement = "Right"

        if movement:
            return Node(data=new_state, parent=self, origin=movement, depth=self.depth+1)

        return False

    def move(self, new_pos):
        new_state = []

        for i, element in enumerate(self.data):
            if i == self.index:  # index is the OLD LINEAR POS
                new_state.append(self.data[new_pos])
            elif i == new_pos:
                new_state.append(0)
            else:
                new_state.append(element)

        return tuple(new_state)

    def print(self):
        print("\n", self.origin)
        for i, element in enumerate(self.data):
            print(element, end=' ')
            # if i > self.n and float((i+1) % self.n) != 0:
            if float((i+1) % self.n == 0) and i < len(self.data)-1:
                print("\n")


def main():
    # initial_state = (4, 2, 3, 6, 5, 9, 12, 7, 1, 13, 11, 15, 8, 10, 14, 0)
    #initial_state = (9, 6, 5, 2, 1, 4, 7, 3, 8, 12, 0, 11, 14, 13, 10, 15)

    method = str(sys.argv[1])
    initial_state = tuple(int(n) for n in sys.argv[2].split(','))

    solver = Solver(initial_state, method)
    solver.run()
    solver.create_output()
    print_file("output.txt")


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


def print_file(file_name):
    f = open(file_name, 'r')
    message = f.read()
    print(file_name, message, '', sep='\n---------------------------------------\n')
    f.close()


if __name__ == '__main__':
    main()



