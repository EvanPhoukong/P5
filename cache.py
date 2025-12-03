"""
"""

import argparse, sys, math, os
from pathlib import Path

def input_error_handling(args):
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--type', type=str, choices=['d', 's'])
    parser.add_argument('--nway', type=int, nargs='?')
    parser.add_argument('--cache_size', type=int)
    parser.add_argument('--block_size', type=int)
    parser.add_argument('--memfile', type=str) 

    args = vars(parser.parse_args())

    input_error_handling(args)

    print(args.items())

    # processor = Processor()

    # store_addrs(args['program'])

    # store_memory(args['memory'])
