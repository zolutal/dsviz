from dsviz.gdb import Gdb
from dsviz.types import Struct
from dsviz.graph import Graph

import argparse
import sys

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("dsviz")
    parser.add_argument('path', type=str, help="The path of the binary to run dsviz on")
    parser.add_argument('name', type=str, help="The name of the type from the debug info to analyze")
    parser.add_argument('out', type=str, nargs='?', help="Optional path to save the visualization to")
    return parser.parse_args(sys.argv[1:])

def main():
    ns: argparse.Namespace = parse_args()

    gdb = Gdb()
    gdb.add_symbol_file(ns.path)

    type_obj: Struct = gdb.find_struct(ns.name)
    type_obj.init_fields()

    Graph(type_obj, ns.out)
