from dsviz.gdb import Gdb
from dsviz.types import Struct
from dsviz.graph import Graph
import pathlib
import sys

def main():
    if len(sys.argv) < 2:
        raise Exception("Invalid arguments for command, expected PATH")
    if len(sys.argv) < 3:
        raise Exception("Invalid arguments for command, expected SYMBOL")

    outfile = None
    if len(sys.argv) == 4:
        outfile = sys.argv[3]

    gdb = Gdb()

    obj_path = sys.argv[1]
    gdb.add_symbol_file(obj_path)

    type_name = sys.argv[2]
    type_obj: Struct = gdb.find_struct(type_name)
    type_obj.init_fields()

    g = Graph(type_obj, outfile)