import math


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
