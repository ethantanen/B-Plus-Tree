import math
import pprint
import node


class Interior(node.Node):

    def __init__(self, children):
        self.children = children
        self.compute_values()

    # determine the values of an interior node based on its subtrees valeus
    def compute_values(self):
        self.fanout = len(self.children)
        self.values = [None] + \
            [self.children[i - 1].maximum() for i in range(1, self.fanout)]

    # determine the maximum value of a node based on its subtrees value (returns once the recursion has hit a leaf node)
    def maximum(self):
        return self.children[self.fanout - 1].maximum()

    def overflow(self):
        return self.fanout > self.order

    # select the correct child sub-tree for the given value
    def select_child(self, value):
        for i in range(1, self.fanout):
            if value <= self.values[i]:
                return i - 1, self.children[i - 1]
        else:  # part of the for-loop (indentation is critical here)
            return i, self.children[i]

    def insert(self, value):
        pos, child = self.select_child(value)
        node = child.insert(value)
        if node != child:
            # child has been replaced with a new Interior node
            # compute new list of children for this node
            self.children = self.children[: pos] + node.children + \
                self.children[pos + 1:]
        # must update own values as children's values have changed
        self.compute_values()
        return self.split()

    def split(self):
        if not self.overflow():
            return self
        half = int(math.ceil(self.fanout / 2.0))
        new_1 = self.__class__(self.children[: half])
        new_2 = self.__class__(self.children[half:])
        return self.__class__([new_1, new_2])

    def get(self):
        result = []
        for i in range(self.fanout):
            result += self.children[i].get()
        return result

    def depth(self):
        return 1 + max([child.depth() for child in self.children])


    def delete(self, value, left_neigh=None, right_neigh=None, left_anchor=None, right_anchor=None):

        # determine next node to visit
        pos, child = self.select_child(value)

        # determine child's neighbors and anchors
        child_left_neigh, child_left_anchor, child_right_neigh, child_right_anchor = \
            self.get_nexts(left_neigh, right_neigh, left_anchor, right_anchor, pos, child)

        # continue recursive search
        child = child.delete(value, child_left_neigh, child_right_neigh, child_left_anchor, child_right_anchor)

        #NOTE: at this point in the execution the algorithm has reached its base case and the call stack is
        # beginning to shrink (unwind)

        # check if rebalance or merge is necessary
        if child.is_at_least_half_full():
            # no rebalnce or merge is necessary
            # update current nodes pointers
            self.compute_values()
            return self

        # check if rebalance is possible than check if merge is possible
        if child_left_neigh and child_left_neigh.rebalance(child):
            pass
        elif child.rebalance(child_right_neigh):
            pass
        elif child.merge(child_left_neigh):
            # remove the empty child from the current node
            self.children.remove(child)
        elif child.merge(child_right_neigh):
            # remove the emtpy child from the current node
            self.children.remove(child)

        # update current nodes pointers after rebalance/ merge
        self.compute_values()

        # check for root conditions
        if len(self.children) <= 1:
            return self.children[0]

        return self

    # merge this nodes children with the node passed in
    def merge (self, node):

        # check if node exists and that a merge will not cause an overflow scenario
        if not node or len(node.children) + len(self.children) > self.order:
            return False

        # add this nodes children to node's children and remove children from this node
        # node.children will be less than self.children
        node.children += self.children
        self.children = []

        # confirm that a merge occured
        return True

    # rebalance this node with the node passed in
    def rebalance(self, node):

        # check if rebalance is possible
        if not node or not node.is_at_least_half_full():
            return False

        # combine value lists and determine halfway point
        children = self.children + node.children
        half = math.floor(len(children)/2)

        # update nodes
        self.values = children[:half]
        node.values = children[half:]

        # confirm that a rebalance occured
        return True


    # determine if a node is at least halfway full
    def is_at_least_half_full(self):
        return len(self.children) >= math.floor(self.order/2)

    # calculate the next_nodes neighbors and anchors
    # anchors are the nodes at which a node and its neighbor branch off
    # next_node_pos is the index of the child in the parent's children array
    def get_nexts(self, left_node, right_node, left_anchor, right_anchor, next_node_pos, next_node):

         # calculate next left node and its anchor
        if next_node is self.get_least_pointer():
            next_left =  left_node.get_greatest_pointer() if left_node else None
            next_left_anchor = left_anchor
        else:
            next_left = self.children[next_node_pos-1]
            next_left_anchor = node

        # calculate next right node and its anchor
        if next_node is self.get_greatest_pointer():
            next_right = right_node.get_least_pointer() if right_node else None
            next_right_anchor = right_anchor
        else:
            next_right = self.children[next_node_pos+1]
            next_right_anchor = node

        return next_left, next_left_anchor, next_right, next_right_anchor

    # return the greatest child in the childrens array
    def get_greatest_pointer(self):
        return self.children[-1]

    # retrun the least child in the childrens array
    def get_least_pointer(self):
        return self.children[0]

    # check is for verification that the node is consistent
    def check(self):
        [child.check() for child in self.children]
        assert self.fanout == len(self.children) == len(self.values)
        assert not self.overflow()
        for i in range(self.fanout - 1):
            assert self.children[i].maximum() == self.values[i + 1]

    # walk is for debugging only
    def walk(self, level=0):
        print("level:", level, sep=" ", end=" ")
        pprint.pprint(self)
        for i in range(self.fanout):
            print("\t", self.values[i], self.children[i], sep=" ")
        for i in range(self.fanout):
            self.children[i].walk(level + 1)
