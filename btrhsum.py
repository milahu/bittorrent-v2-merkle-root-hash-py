#!/usr/bin/env python3

import hashlib
import math



def get_bt2_leaf_hash_list_of_path(file_path):

    """
    get bittorrent v2 merkle root leaf hash list of file path
    """

    nodes = []

    chunk_size = 16 * 1024

    with open(file_path, "rb") as f:

        # TODO better. this needs much memory for large files
        while chunk := f.read(chunk_size):
            leaf_node = hashlib.sha256(chunk).digest()
            nodes.append(leaf_node)

    return nodes



def get_bt2_root_hash_of_path(file_path):

    """
    get bittorrent v2 merkle root hash of file path
    """

    # sha256 performance https://stackoverflow.com/questions/67355203/how-to-improve-the-speed-of-merkle-root-calculation

    nodes = get_bt2_leaf_hash_list_of_path(file_path)

    if True:

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

    if len(sys.argv) == 1:
        print("usage:", file=sys.stderr)
        print("", file=sys.stderr)
        print("  get bt2 root hash of file:", file=sys.stderr)
        print("", file=sys.stderr)
        print(f"    {sys.argv[0]} file_path", file=sys.stderr)
        print("", file=sys.stderr)
        print("  get bt2 leaf hashes of file:", file=sys.stderr)
        print("", file=sys.stderr)
        print(f"    {sys.argv[0]} -l file_path", file=sys.stderr)
        print(f"    {sys.argv[0]} --leaf-hashes file_path", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] in ["-l", "--leaf-hashes"]:
        file_path = sys.argv[2]
        for digest in get_bt2_leaf_hash_list_of_path(file_path):
            print(digest.hex())
        sys.exit()

    file_path = sys.argv[1]
    print(get_bt2_root_hash_of_path(file_path).hex())
