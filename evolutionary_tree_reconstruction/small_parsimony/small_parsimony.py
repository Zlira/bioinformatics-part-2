"""
Implement SmallParsimony to solve the Small Parsimony Problem.
Input: An integer n followed by an adjacency list for a rooted binary tree
    with n leaves labeled by DNA strings.
Output: The minimum parsimony score of this tree, followed by the adjacency
    list of the tree corresponding to labeling internal nodes by DNA strings
    in order to minimize the parsimony score of the tree.
"""
from collections import defaultdict
import sys


BASES = ('A', 'T', 'C', 'G')
EDGE_SYMBOL = '->'


class Tree(defaultdict):
    """
    This class represents a rooted binary tree. Each node is a key
    in a dictionary and it's value is list of all nodes it is
    connected to.
    """

    def __init__(self, *args, **kwargs):
        return super(Tree, self).__init__(list, *args, **kwargs)

    def __str__(self):
        return '\n'.join([
            '{} -> {}'.format(start, end) for start, ends in self.items()
            for end in ends
        ])


class Node:
    """
    This is a node of a Tree. It has an integer lable as well as
    nucleotide sequence associated with it.
    """

    def __init__(self, lable, sequence=None):
        self.lable = lable
        self.sequence = sequence

    def __hash__(self):
        return hash(self.lable)

    def __str__(self):
        return self.sequence if self.sequence else str(self.lable)

def main():
    with open(sys.argv[1]) as input_file:
        leaves_num = int(input_file.readline().rstrip())
        count = 0
        tree = Tree()
        for line in input_file:
            key, val = line.rstrip().split(EDGE_SYMBOL)
            key = Node(lable=int(key))
            if len(val) > 1:
                val = Node(lable=count, sequence=val)
                count += 1
            else:
                val = Node(lable=val)
            tree[key].append(val)
    print(tree)

if __name__ == '__main__':
    main()
