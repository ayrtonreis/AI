from Node import Node
from collections import deque
from heapq import heappush, heappop
import time
import sys

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

        print('GOAL STATE: ', self.goal_state, "    -    ", self.method.upper())


    def create_output(self):
        '''back_track = self.last_node

        while back_track.parent != None:
            back_track.print()
            #print("  D = ", back_track.depth, "   TC = ", back_track.total_cost, "   h= ", back_track.total_cost- back_track.depth)
            back_track = back_track.parent'''

        self.handle_output(path=self.path_to_goal, cost=self.last_node.total_cost, expanded=self.expanded, fringe_size=self.fringe_size, max_fringe_size=self.max_fringe_size,depth=self.last_node.depth, max_depth=self.max_search_depth, running_time=self.stop_time)

    def handle_output(self,path=[], cost='*', expanded='*', fringe_size='*', max_fringe_size='*', depth='*', max_depth='*',
                      running_time='*', ram='*'):
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
        file.write("max_ram_usage: " + '{}'.format(ram))
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
        # self.expanded = 0  # re-count for ida for each iteration?
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