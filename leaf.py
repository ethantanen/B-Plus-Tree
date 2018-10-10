import math
import pprint
import node
import interior


class Leaf(node.Node):

    def __init__(self, values):
        self.values = values
        self.nvalues = len(values)
        # minimum number of values in leaf node
        self.minimum = int(math.floor((self.order - 1) / 2.0))

    def maximum(self):
        return self.values[self.nvalues - 1]

    def overflow(self):
        # order at leaf node is 1 less than order at other kinds of nodes
        # per textbook
        return self.nvalues >= self.order

    def insert(self, value):
        # ignore duplicate values
        if value in self.values:
            return self
        else:
            self.values.append(value)
            self.values.sort()
            self.nvalues += 1
            return self.split()

    def split(self):
        if not self.overflow():
            return self
        half = int(math.ceil(self.nvalues / 2.0))
        new_1 = self.__class__(self.values[: half])
        new_2 = self.__class__(self.values[half:])
        return interior.Interior([new_1, new_2])

    def get(self):
        return self.values

    def depth(self):
        return 1

    def delete(self, value, left=None, right=None, left_anchor=None, right_anchor=None):
        if value in self.values:
            self.values.remove(value)
            self.nvalues -= 1
        return self


    # merges self with node (left merge)
    def merge(self, node):

        # check if merge is possible
        if not node or node.nvalues + self.nvalues > self.order:
            return False

        # move content of current node to node and update nvalues
        node.nvalues += self.nvalues
        node.values += self.values
        node.values.sort()

        # erase content of current node
        self.values = []
        self.nvalues = 0

        print(node.values, self.values)
        return True


    # rebalances by moving content from node to this node
    def rebalance(self, node):

        # reject rebalance if node is halfway full
        if not node or self.nvalues + node.nvalues < 2*math.floor(self.order/2):
            return False

        # combine value lists and determine halfway point
        values = (self.values + node.values)
        values.sort()
        half = math.floor(len(values)/2)

        # update current node
        self.values = values[:half]
        self.nvalues = len(self.values)

        # update other node
        node.values = values[half:]
        node.nvalues = len(node.values)

        return True


    def is_more_than_half_full(self):
        return self.nvalues >= math.floor(self.order/2)


    def check(self):
        assert self.nvalues == len(self.values)
        assert not self.overflow() and self.nvalues >= self.minimum
        for i in range(1, self.nvalues):
            assert self.values[i - 1] < self.values[i]

    # walk is for debugging only
    def walk(self, level=0):
        print("level:", level, sep=" ", end=" ")
        pprint.pprint(self)
        for i in range(self.nvalues):
            print("\t", self.values[i], sep=" ", end="")
        print(end="\n")
