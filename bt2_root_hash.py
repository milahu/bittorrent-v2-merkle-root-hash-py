#!/usr/bin/env python3

import hashlib
import math

def get_bt2_root_hash_of_path(file_path):
    """
    get bittorrent v2 merkle root hash of file path
    """

    with open(file_path, "rb") as f:

        # sha256 performance https://stackoverflow.com/questions/67355203/how-to-improve-the-speed-of-merkle-root-calculation

        """
        # libtorrent
        def merkle_pad(blocks, pieces):
            ret = b"\x00" * 32
            while pieces < blocks:
                ret = hashlib.sha256(ret + ret).digest()
                pieces *= 2
            return ret
        default_block_size = 16 * 1024
        # wrong callsite of merkle_pad?
        pad_hash = merkle_pad(m_files.piece_length() / default_block_size, 1)

        # sha256_hash const pad_hash = merkle_pad(1 << m_blocks_per_piece_log, 1);

        merkle_root(pieces, pad_hash)
        """

        # how to calculate the root hash?

        # http://bittorrent.org/beps/bep_0030.html
        # Merkle hash torrent extension
        # From the content we construct a hash tree as follows.
        # Given a piece size, we calculate the hashes of all the pieces in the set of content files.
        #   note: with bt2, the piece size constant at 16 KiB
        # Next, we create a binary tree of sufficient height.
        # Sufficient height means that the lowest level in the tree has enough nodes to hold all piece hashes in the set.
        # We place all piece hashes in the tree, starting at the left-most leaf.
        # The remaining leaves in the tree are assigned a filler hash value of 0.
        # Finally, we calculate the hash values of the higher levels in the tree,
        # by concatenating the hash values of the two children (again left to right)
        # and computing the hash of that aggregate.
        # This process ends in a hash value for the root node, which we call the root hash.
        # The hashing algorithm used is SHA1, as in normal torrents.
        #   note: with bt2, the hashing algorithm is SHA256

        # https://blog.libtorrent.org/2020/09/bittorrent-v2/
        # The leaves of the hash trees are always 16 kiB (the block size)

        # https://github.com/kovalensky/tmrr/blob/main/tmrr.php
        # $hash = new HasherV2($file);
        # $hash->root
        # $this->root = bin2hex($this->merkle_root($this->layer_hashes));


        # https://github.com/topics/merkle-tree?l=python

        if False:
            import merkletools
            mt = merkletools.MerkleTools(hash_type="sha256")
            chunk_size = 16 * 1024 # == 16384
            chunk_size = torrent_piece_length
            do_hash = True
            #do_hash = False
            while chunk := f.read(chunk_size):
                mt.add_leaf(chunk.hex(), do_hash)
            mt.make_tree()
            root_value = mt.get_merkle_root()
            print("root_value", root_value)
            raise Exception("todo")

        if False:
        #if True:
            # pymerkle
            # https://github.com/fmerg/pymerkle
            from pymerkle import InmemoryTree as MerkleTree
            tree = MerkleTree(algorithm='sha256')
            chunk_size = 16 * 1024 # == 16384
            chunk_size = torrent_piece_length
            while chunk := f.read(chunk_size):
                tree.append_entry(chunk)
            state = tree.get_state() # current root-hash
            print("tree state", state.hex())
            size = tree.get_size() # number of leaves
            print("tree size", size) # 378 -> ok
            raise Exception("todo")

        if False:
        #if True:
            from merklelib import MerkleTree
            def hashfunc(value):
                return hashlib.sha256(value).hexdigest()
            chunk_list = []
            chunk_size = 16 * 1024 # == 16384
            #chunk_size = torrent_piece_length
            while chunk := f.read(chunk_size):
                chunk_list.append(chunk)
            tree = MerkleTree(chunk_list, hashfunc)
            print("asdf", tree.merkle_root)
            raise Exception("todo")



        #if True:
        if False:
            # https://github.com/kovalensky/tmrr/blob/main/tmrr.php
            # this gives the correct result, but there is some unreachable code

            # private function merkle_root($blocks)
            def merkle_root(blocks):
                # while (count($blocks) > 1) {
                while len(blocks) > 1:
                    # $blocks_count = count($blocks);
                    blocks_count = len(blocks)
                    # always a power of 2
                    print(f"merkle_root: blocks_count = {blocks_count}")
                    # $next_level_blocks = [];
                    next_level_blocks = []
                    # $i = 0;
                    i = 0
                    # while ($i < $blocks_count) {
                    while i < blocks_count:
                        # $x = $blocks[$i];
                        x = blocks[i]
                        # $y = ($i + 1 < $blocks_count) ? $blocks[$i + 1] : '';
                        y = blocks[i + 1] if i + 1 < blocks_count else b"" # note: different padding
                        # expected: next hash f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b
                        # actual:   next hash 60e05bd1b195af2f94112fa7197a5c88289058840ce7c6df9693756bc6250f55

                        #y = blocks[i + 1] if i + 1 < blocks_count else (b"\x00" * 32) # zero padding
                        # expected: next hash f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b
                        # actual:   next hash 60e05bd1b195af2f94112fa7197a5c88289058840ce7c6df9693756bc6250f55

                        # debug
                        # not reached
                        if i + 1 == blocks_count:
                            print(f"adding padding at i = {i} vs blocks_count = {blocks_count}")
                        print(f"next hash = hash({x.hex()} + {y.hex()}) =", hashlib.sha256(x + y).digest().hex())
                        # $next_level_blocks[] = hash('sha256', $x . $y, true);
                        next_level_blocks.append(hashlib.sha256(x + y).digest())
                        # $i += 2;
                        i += 2
                    # $blocks = $next_level_blocks;
                    blocks = next_level_blocks
                # return $blocks[0];
                return blocks[0]

            # $this->num_blocks = 1;
            num_blocks = 1 # const. num_blocks is always 1

            # $piece_length = 16384) // 16KiB blocks
            # define('BLOCK_SIZE', $piece_length);
            chunk_size = 16 * 1024 # == 16384

            # define('HASH_SIZE', 32);

            # $this->layer_hashes = [];
            layer_hashes = []

            #block_list = []
            # 706a857a672192149ad1cb83df3215dba3d2f8628187595363054caab12cdde2

            # $leaf = fread($fd, BLOCK_SIZE);
            while chunk := f.read(chunk_size):

                # this is wrong? move out of while loop
                # $blocks = [];
                block_list = []
                # 532b88283bf68cb1c8a3842fbe3146aeae9b45cfbc89f2dbbd0b1bdf649305bd

                # $blocks[] = hash('sha256', $leaf, true);
                block_list.append(hashlib.sha256(chunk).digest())

                # $blocks_count = count($blocks);
                blocks_count = len(block_list)

                # always 1
                if blocks_count != 1:
                    print("len(block_list)", len(block_list))

                # if ($blocks_count !== $this->num_blocks) {
                if blocks_count != 1:

                    # $remaining = $this->num_blocks - $blocks_count;
                    remaining = 1 - blocks_count

                    # if (count($this->layer_hashes) === 0) {
                    if len(layer_hashes) == 0:

                        # $power2 = next_power_2($blocks_count);
                        power2 = 2**math.ceil(math.log2(blocks_count))

                        # not reached
                        # $remaining = $power2 - $blocks_count;
                        remaining = power2 - blocks_count
                        print("remaining", remaining)

                    # stupid error: b"0" != b"\x00"
                    # >>> (b"0" * 32).hex()
                    # '3030303030303030303030303030303030303030303030303030303030303030'
                    # >>> (b"\x00" * 32).hex()
                    # '0000000000000000000000000000000000000000000000000000000000000000'

                    # $padding = array_fill(0, $this->num_blocks, str_repeat("\x00", HASH_SIZE));
                    padding = [b"\x00" * 32]

                    # not reached
                    # $blocks = [...$blocks, ...array_slice($padding, 0, $remaining)];
                    print("len(block_list) a", len(block_list))
                    block_list += padding * remaining
                    print("len(block_list) b", len(block_list))

                # $layer_hash = $this->merkle_root($blocks);
                layer_hash = merkle_root(block_list)

                # ok
                #print("layer_hash", layer_hash.hex())

                # $this->layer_hashes[] = $layer_hash;
                layer_hashes.append(layer_hash)

            # $this->calculate_root();
            # private function calculate_root()
            def calculate_root(layer_hashes):
                # $this->piece_layer = implode('', $this->layer_hashes);
                # not needed
                #piece_layer = b"".join(layer_hashes)
                # $hashes = count($this->layer_hashes);
                hashes = len(layer_hashes)
                # if ($hashes > 1) {
                if hashes > 1:
                    # $pow2 = $this->next_power_2($hashes);
                    power2 = 2**math.ceil(math.log2(hashes))
                    # $remainder = $pow2 - $hashes;
                    remaining = power2 - hashes
                    # $pad_piece = array_fill(0, $this->num_blocks, str_repeat("\x00", HASH_SIZE));
                    padding = [b"\x00" * 32]
                    # while ($remainder > 0) {
                    while remaining > 0:
                        # $this->layer_hashes[] = $this->merkle_root($pad_piece);
                        layer_hashes.append(merkle_root(padding))
                        # $remainder--;
                        remaining -= 1
                # $this->root = bin2hex($this->merkle_root($this->layer_hashes));
                return merkle_root(layer_hashes).hex()

            print("root", calculate_root(layer_hashes))
            # ok
            raise Exception("todo")
            # 532b88283bf68cb1c8a3842fbe3146aeae9b45cfbc89f2dbbd0b1bdf649305bd # actual, different padding
            # 532b88283bf68cb1c8a3842fbe3146aeae9b45cfbc89f2dbbd0b1bdf649305bd # actual, zero padding
            # 81a9139f09683032072123c66ef9b56c5adc18ed3d833024ef2c2f90f2295445 # expected





        # https://stackoverflow.com/questions/70316918/how-to-implement-merkle-hash-tree-in-python
        # ^ does not handle odd length, should duplicate last leaf node

        # https://stackoverflow.com/questions/61738723/code-to-compute-the-merkle-root-for-the-block
        # endian swap

        # libtorrent/src/merkle.cpp

        #  // compute the merkle tree root, given the leaves and the has to use for
        #  // padding
        #  sha256_hash merkle_root_scratch(span<sha256_hash const> leaves
        #    , int num_leafs, sha256_hash pad
        #    , std::vector<sha256_hash>& scratch_space)
        #  {

        #  if (leaves.size() & 1)
        #  {
        #    // if we have an odd number of leaves, compute the boundary hash
        #    // here, that spans both a payload-hash and a pad hash
        #    scratch_space[std::size_t(i)] = hasher256()
        #      .update(leaves[i * 2])
        #      .update(pad)
        #      .final();
        #    ++i;
        #  }

        #  // generates the pad hash for the tree level with "pieces" nodes, given the
        #  // full tree has "blocks" number of blocks.
        #  sha256_hash merkle_pad(int blocks, int pieces)
        #  {
        #    TORRENT_ASSERT(blocks >= pieces);
        #    sha256_hash ret{};
        #    while (pieces < blocks)
        #    {
        #      hasher256 h;
        #      h.update(ret);
        #      h.update(ret);
        #      ret = h.final();
        #      pieces *= 2;
        #    }
        #    return ret;
        #  }

        # libtorrent/src/create_torrent.cpp

        #  sha256_hash const pad_hash = merkle_pad(m_files.piece_length() / default_block_size, 1);
        #
        #  m_fileroots[fi] = merkle_root(m_file_piece_hash[fi], pad_hash);

        leaf_list = []

        chunk_size = 16 * 1024 # ok
        #chunk_size = torrent_piece_length

        use_text_hashes = False # ok
        #use_text_hashes = True

        odd_node = "ignore" # no
        odd_node = "repeat" # no
        odd_node = "pad" # no
        pad_full = True # ok
        #pad_full = False

        pad_with_zero_hashes = False
        pad_with_zero_hashes = True # ok

        pad_chunk = False # ok
        #pad_chunk = True

        # endian swap
        endian_swap = False # ok
        #endian_swap = True

        # TODO better. this needs much memory for large files
        while chunk := f.read(chunk_size):
            if pad_chunk:
                if len(chunk) < chunk_size:
                    missing_len = chunk_size - len(chunk)
                    chunk += b"\x00" * missing_len
            if endian_swap == False:
                if use_text_hashes:
                    leaf = hashlib.sha256(chunk).hexdigest() # text hashes
                else:
                    leaf = hashlib.sha256(chunk).digest() # binary hashes
            else:
                if use_text_hashes:
                    leaf = hashlib.sha256(chunk[::-1]).hexdigest()[::-1] # text hashes
                else:
                    leaf = hashlib.sha256(chunk[::-1]).digest()[::-1] # binary hashes
            leaf_list.append(leaf)
        nodes = leaf_list

        # TODO better, use less memory
        if pad_full:
            #print("len nodes", len(nodes))
            # len nodes 378
            # next 2**n number is 512
            # 2**math.ceil(math.log2(378)) == 512
            if pad_with_zero_hashes:
                if use_text_hashes:
                    empty_digest = "0" * 64
                else:
                    empty_digest = b"\x00" * 32
            else:
                if endian_swap == False:
                    if use_text_hashes:
                        empty_digest = hashlib.sha256(b"\x00" * chunk_size).hexdigest()
                    else:
                        empty_digest = hashlib.sha256(b"\x00" * chunk_size).digest()
                else:
                    if use_text_hashes:
                        empty_digest = hashlib.sha256(b"\x00" * chunk_size).hexdigest()[::-1]
                    else:
                        empty_digest = hashlib.sha256(b"\x00" * chunk_size).digest()[::-1]
            num_missing_nodes = 2**math.ceil(math.log2(len(nodes))) - len(nodes)
            nodes += [empty_digest] * num_missing_nodes

        #raise Exception("todo")

        while len(nodes) != 1:
            next_nodes = []
            for i in range(0, len(nodes), 2):
                node1 = nodes[i]
                if i+1 < len(nodes):
                    node2 = nodes[i+1]
                else:
                    # odd length
                    assert pad_full == False # this should never happen with pad_full == True
                    if odd_node == "repeat":
                        # repeat odd node
                        node2 = node1
                    elif odd_node == "ignore":
                        next_nodes.append(nodes[i])
                        break
                    elif odd_node == "pad":
                        if use_text_hashes:
                            node2 = "0" * 64
                        else:
                            node2 = b"\x00" * 64
                        # this is wrong. we need a perfect binary tree with 2**n leaf nodes

                #f.write("Left child : "+ node1.value + " | Hash : " + node1.hashValue +" \n")
                #f.write("Right child : "+ node2.value + " | Hash : " + node2.hashValue +" \n")
                #concatenatedHash = node1.hashValue + node2.hashValue
                if endian_swap == False:
                    concatenatedHash = node1 + node2
                else:
                    concatenatedHash = node1[::-1] + node2[::-1]
                #parent = MerkleTreeNode(concatenatedHash)
                if use_text_hashes:
                    parent = hashlib.sha256(concatenatedHash.encode('ascii')).hexdigest() # text hashes
                else:
                    parent = hashlib.sha256(concatenatedHash).digest() # binary hashes
                if endian_swap == True:
                    parent = parent[::-1]
                #parent.left = node1
                #parent.right = node2
                #f.write("Parent(concatenation of "+ node1.value + " and " + node2.value + ") : " +parent.value + " | Hash : " + parent.hashValue +" \n")
                next_nodes.append(parent)
            nodes = next_nodes
        #return nodes[0]
        root_node = nodes[0]
        return root_node


if __name__ == "__main__":
    import sys
    file_path = sys.argv[1]
    print(get_bt2_root_hash_of_path(file_path).hex())
