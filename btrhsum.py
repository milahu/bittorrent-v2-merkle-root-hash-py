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

    output_format = "hex"
    leaf_hashes = False
    file_path = None

    for arg in sys.argv[1:]:
        if arg in ["-l", "--leaf-hashes"]:
            leaf_hashes = True
            continue
        if arg in ["-b", "--binary"]:
            output_format = "binary"
            continue
        if arg in ["--base64"]:
            output_format = "base64"
            continue
        if file_path != None:
            printf("error: multiple input files. please pass only one input file", file=sys.stderr)
            sys.exit(1)
        file_path = arg

    digest_list = []

    if leaf_hashes:
        digest_list = get_bt2_leaf_hash_list_of_path(file_path)
    else:
        digest_list = [get_bt2_root_hash_of_path(file_path)]

    if output_format == "hex":
        for digest in digest_list:
            print(digest.hex())
        sys.exit(0)

    if output_format == "base64":
        import base64
        for digest in digest_list:
            print(base64.b64encode(digest).decode("ascii"))
        sys.exit(0)

    if output_format == "binary":
        for digest in digest_list:
            sys.stdout.buffer.write(digest)
        sys.exit(0)
