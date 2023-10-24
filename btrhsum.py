#!/usr/bin/env python3

import hashlib
import math



def get_bt2_leaf_hash_list_of_path(file_path):

    """
    get bittorrent v2 merkle root leaf hash list of file path
    """

    leaf_hash_list = []

    chunk_size = 16 * 1024

    with open(file_path, "rb") as f:

        # TODO better. this needs much memory for large files
        while chunk := f.read(chunk_size):
            leaf_hash = hashlib.sha256(chunk).digest()
            yield leaf_hash



def get_bt2_root_hash_of_path(file_path):

    """
    get bittorrent v2 merkle root hash of file path
    """

    leaf_hash_list = list(get_bt2_leaf_hash_list_of_path(file_path))

    return get_bt2_root_hash_of_leaf_hash_list(leaf_hash_list)



def get_bt2_root_hash_of_leaf_hash_list(leaf_hash_list):

    """
    get bittorrent v2 merkle root hash of leaf hash list
    """

    # sha256 performance https://stackoverflow.com/questions/67355203/how-to-improve-the-speed-of-merkle-root-calculation

    # copy to preserve the original list
    nodes = leaf_hash_list[:]

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
    import os
    import base64

    if len(sys.argv) == 1:
        arg0 = os.path.basename(sys.argv[0])
        print("\n".join([
            "usage:",
            "",
            "  get hex bt2 root hash of file:",
            "",
            f"    {arg0} file_path",
            "",
            "  get hex bt2 leaf hashes of file:",
            "",
            f"    {arg0} -l file_path",
            f"    {arg0} --leaf-hashes file_path",
            "",
            "  get hex bt2 all (leaf and root) hashes of file:",
            "",
            f"    {arg0} -a file_path",
            f"    {arg0} --all-hashes file_path",
            "",
            "  get base64 bt2 root hash of file:",
            "",
            f"    {arg0} --base64 file_path",
            "",
            "  get binary bt2 root hash of file:",
            "",
            f"    {arg0} -b file_path",
            f"    {arg0} --binary file_path",
        ]), file=sys.stderr)
        sys.exit(1)

    leaf_hashes = False
    all_hashes = False
    file_path = None

    def print_hash_hex(hash):
        print(hash.hex())

    def print_hash_base64(hash):
        print(base64.b64encode(hash).decode("ascii"))

    def print_hash_binary(hash):
        sys.stdout.buffer.write(hash)

    print_hash = print_hash_hex

    for arg in sys.argv[1:]:
        if arg in ["-a", "--all-hashes"]:
            all_hashes = True
            continue
        if arg in ["-l", "--leaf-hashes"]:
            leaf_hashes = True
            continue
        if arg in ["-b", "--binary"]:
            print_hash = print_hash_binary
            continue
        if arg in ["--base64"]:
            print_hash = print_hash_base64
            continue
        if file_path != None:
            print("error: multiple input files. please pass only one input file", file=sys.stderr)
            sys.exit(1)
        file_path = arg

    if all_hashes:
        leaf_hash_list = []
        for leaf_hash in get_bt2_leaf_hash_list_of_path(file_path):
            print_hash(leaf_hash)
            leaf_hash_list.append(leaf_hash)
        if len(leaf_hash_list) > 1:
            root_hash = get_bt2_root_hash_of_leaf_hash_list(leaf_hash_list)
            print_hash(root_hash)
    elif leaf_hashes:
        for leaf_hash in get_bt2_leaf_hash_list_of_path(file_path):
            print_hash(leaf_hash)
    else:
        root_hash = get_bt2_root_hash_of_path(file_path)
        print_hash(root_hash)
