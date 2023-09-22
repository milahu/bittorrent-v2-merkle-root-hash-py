#!/usr/bin/env python3

import hashlib
import math



def get_bt2_root_hash_of_path(file_path):

    """
    get bittorrent v2 merkle root hash of file path
    """

    # sha256 performance https://stackoverflow.com/questions/67355203/how-to-improve-the-speed-of-merkle-root-calculation

    nodes = []

    chunk_size = 16 * 1024

    with open(file_path, "rb") as f:

        # TODO better. this needs much memory for large files
        while chunk := f.read(chunk_size):
            leaf_node = hashlib.sha256(chunk).digest()
            nodes.append(leaf_node)

        # pad tree to binary tree
        # TODO better. use less memory
        empty_digest = b"\x00" * 32
        num_missing_nodes = 2**math.ceil(math.log2(len(nodes))) - len(nodes)
        nodes += [empty_digest] * num_missing_nodes

        while len(nodes) != 1:
            next_nodes = []
            for i in range(0, len(nodes), 2):
                node1 = nodes[i]
                # tree was padded to binary tree, so nodes[i+1] is always defined
                node2 = nodes[i+1]
                parent_node = hashlib.sha256(node1 + node2).digest()
                next_nodes.append(parent_node)
            nodes = next_nodes
        return nodes[0]



if __name__ == "__main__":

    import sys

    file_path = sys.argv[1]
    print(get_bt2_root_hash_of_path(file_path).hex())
