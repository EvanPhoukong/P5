"""
This module simulates the behavior of a direct-mapped cache or n-way set associative cache for a sequence
of memory access of 4-byte words, using 32-bit addresses.
"""

import argparse, sys, math, os
from pathlib import Path


class Cache:

    def __init__(self, blocks):
        self.blocks = {format(block, '02b'): None for block in range(blocks)}

    def get_block(self, index):
        return self.blocks[index]
    
    def set_block(self, index, tag):
        self.blocks[index] = tag


class Block:
    "A block in the cache. Only the tag bit is tored"

    def __init__(self):
        """
        Initialize class and tag member variable
        """
        self.tag = None
        pass

    def set_tag(self, tag):
        """
        Set the tag value
        """
        self.tag = tag


    def get_tag(self):
        """
        Get the tag value
        """
        return self.tag



def input_error_handling(args: dict) -> None:
    """
    The functions handles any errors with the module/teriminal arguments.
    """

    #Handle missing nway parameter for set associative cache simulations
    if args['type'] == 's' and args['nway'] == None:
        print('Set associative cache requires a valid --nway value')
        sys.exit()

    #Handle cache sizes not being a power of 2
    if math.log(args['cache_size'], 2) % 1 != 0:
        print("Cache size must be a power of 2")
        sys.exit()

    #Handle block sizes not being a power of 2
    if math.log(args['block_size'], 2) % 1 != 0:
        print("Block size must be a power of 2")
        sys.exit()

    #Handle block sizes being greater than cache sizes
    if args['block_size'] > args['cache_size']:
        print("Block size must be no greater than total cache size")
        sys.exit()
    
    #Handle file not exising
    if not os.path.exists(args['memfile']):
        print("Unable to open input file")
        sys.exit()


def parse_addr(addr):

    #byte = 30
    word = int(32 - math.log(args['block_size'], 2))
    block = int(word - math.log(args['cache_size'] // args['block_size'], 2))
    print(word, block)

    tag = addr[0 : block]
    index = addr[block : word]
    # word = addr[word: byte]
    # byte = addr[byte : 33]

    return tag, index


def simulate_direct_cache(args, cache):

    hit = 0
    miss = 0

    with open(args['memfile'], 'r') as ifile, open('cache.txt', 'a+', newline ='') as ofile:
        for addr in ifile:
            addr = addr.strip()
            baddr = format(int(addr, 16), '032b')
            tag, index = parse_addr(baddr)
            stored = cache.get_block(index)
            if stored == tag:
                hit += 1
                ofile.write(f'{addr}|{tag}|{index}|HIT\n')
            else:
                miss += 1
                cache.set_block(index, tag)
                ofile.write(f'{addr}|{tag}|{index}|MISS\n')

        hit_rate = 100 * hit/(hit + miss)
        ofile.write(f'\nhit rate:{hit_rate : .1f}')


def main(args):
    
    cache = Cache(args['cache_size'] // args['block_size'])

    if args['type'] == 'd':
        simulate_direct_cache(args, cache)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--type', type=str, choices=['d', 's'])
    parser.add_argument('--nway', type=int, nargs='?')
    parser.add_argument('--cache_size', type=int)
    parser.add_argument('--block_size', type=int)
    parser.add_argument('--memfile', type=str) 

    args = vars(parser.parse_args())

    input_error_handling(args)

    main(args)

    #format(int(a, 16), 'b')