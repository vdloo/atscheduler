#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser
import sys

from atmap import atschedule

def get_args():
    parser = ArgumentParser(description="Schedule 'at' commmands")
    parser.add_argument('command', help='Command to run for all items. More than one \'%%\' possible.')
    parser.add_argument('items', type=str, nargs='+', help='List of items to run the command with. ')
    parser.add_argument('--at', help='Time to start the command(s)', required=True)
    parser.add_argument('--email', help='Address to email the command\'s output to (optional)')
    parser.add_argument('-j', help='Jobs that can run at the same time (default is no limit)', default=0, type=int)
    parser.add_argument('-i', help='Interval in minutes between batches', default=0, type=int)
    return parser.parse_args()

def get_args_from_stdin():
    input_from_stdin = sys.stdin.read()
    return input_from_stdin.split()

def main():
    args = get_args()
    items = get_args_from_stdin() if args.items == ['-'] else args.items
    commands = atschedule(args.command, items, args.at, args.email, parallel=args.j, interval=args.i)
    print(*commands, sep='\n')

if __name__ == '__main__':
    main()
