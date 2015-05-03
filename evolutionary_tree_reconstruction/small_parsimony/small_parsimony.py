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

    def node_is_ripe(self, node):
        return (
            not node.processed and
            all([child.processed for child in self[node]])
        )

    def root(self):
        return max(self.keys(), key=lambda x: x.lable)

    def prit_formated(self):
        for key, vals in self.items():
            for val in vals:
                hum_dist = humming_distance(key.sequence, val.sequence)
                print('{}->{}:{}'.format(key, val, hum_dist))
                print('{}->{}:{}'.format(val, key, hum_dist))


class Node:
    """
    This is a node of a Tree. It has an integer lable as well as
    nucleotide sequence associated with it.
    """

    def __init__(self, lable, sequence=None):
        self.lable = lable
        self.sequence = sequence
        self.processed = False
        self.char_scores = {}

    def __hash__(self):
        return hash(self.lable)

    def __eq__(self, other):
        return self.lable == other.lable

    def __str__(self):
        return self.sequence if self.sequence else str(self.lable)

    def init_char_scores(self):
        if not self.sequence:
            return
        else:
            for index, char in enumerate(self.sequence):
                self.char_scores[index] = {
                    base: 0 if base == char else float('inf') for base in BASES
                }
            self.processed = True

    def best_neighbour_score(self, char, char_index):
        assert self.char_scores, 'Scores for this node are unknown'
        return min([
            score + (0 if base == char else 1) for base, score
            in self.char_scores[char_index].items()
        ])

    def seq_from_char_scores(self):
        self.sequence = ''
        for i in range(len(self.char_scores)):
            self.sequence += min(
                [(base, score) for base, score in self.char_scores[i].items()],
                key=lambda x: x[1]
            )[0]


def humming_distance(seq1, seq2):
    return sum([1 if s1 != s2 else 0 for s1, s2 in zip(seq1, seq2)])


def small_parsimony(tree, seq_len):
    ripe_node = next((
        node for node in tree if tree.node_is_ripe(node)), None
    )
    while ripe_node:
        son, daughter = tree[ripe_node]
        for char_index in range(seq_len):
            ripe_node.char_scores[char_index] = {}
            for base in BASES:
                ripe_node.char_scores[char_index][base] = (
                    daughter.best_neighbour_score(base, char_index) +
                    son.best_neighbour_score(base, char_index)
                )
        ripe_node.processed = True
        ripe_node = next((
            node for node in tree if tree.node_is_ripe(node)), None
        )


def parse_input(input_file_path):
    with open(input_file_path) as input_file:
        leaves_num = int(input_file.readline().rstrip())
        count = 0
        tree = Tree()
        nodes = {}
        for line in input_file:
            key, val = line.rstrip().split(EDGE_SYMBOL)
            if key not in nodes:
                key_obj = Node(lable=int(key))
                nodes[key] = key_obj
            else:
                key_obj = nodes[key]
            if val[0].isalpha():
                val_obj = Node(lable=count, sequence=val)
                count += 1
            else:
                if val not in nodes:
                    val_obj = Node(lable=int(val))
                    nodes[val] = val_obj
                else:
                    val_obj = nodes[val]
            tree[key_obj].append(val_obj)
            if not tree[val_obj]:
                tree[val_obj] = []
    return leaves_num, tree


def main():
    leaves_num, tree = parse_input(sys.argv[1])
    for node in tree:
        node.init_char_scores()
    seq_len = len(next(node.sequence for node in tree if node.sequence))
    small_parsimony(tree, seq_len)
    for node in tree:
        node.seq_from_char_scores()
    print(sum([
        min([val for val in char_values.values()])
        for char_values in tree.root().char_scores.values()])
    )
    tree.prit_formated()

if __name__ == '__main__':
    main()
