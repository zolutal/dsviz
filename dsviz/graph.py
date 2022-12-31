from dsviz.types import Struct, Union
from dsviz.graph_server import GraphServer
from dsviz.const import *

import tempfile
import subprocess

class Graph:
    def __init__(self, root_type, outfile):
        self.nodes = []
        self.edges = []

        self.outfile = outfile
        self.server = GraphServer(
            self,
            row_menu={
                'Expand': lambda node: self.expand_id(node),
            }
        )

        self.add_node(root_type)
        self.server.restart()

    def add_node(self, type):
        self.nodes.append(type)

    def add_edge(self, type, id):
        p_type = type._parent._parent
        p_type_name = p_type.name

        edge = (f"{p_type_name}:{id}", f"{type.name}:{type.name}")
        self.edges.append(edge)

    def find_id(self, id):
        name = id
        idx = None
        if '_' in id:
            split = id.split('_')
            name = '_'.join(split[:-1])
            idx = int(split[-1])

        for node in self.nodes:
            if name in node.name:
                if idx is not None:
                    return node.fields[idx].type
                return node

    def expand_id(self, id):
        if id.startswith('a_'):
            id = id[2:]

        node: Struct = self.find_id(id)
        node.init_fields()

        self.add_node(node)
        self.add_edge(node, id)

        self.server.restart()

    def draw(self):
        digraph_content = ""

        for node in self.nodes:
            digraph_content += graph_node_fmt % (node.name, self.type_table(node))

        for edge in self.edges:
            digraph_content += graph_edge_fmt % edge

        dot_content = graph_header % digraph_content

        f = tempfile.NamedTemporaryFile()
        f.write(dot_content.encode())
        f.flush()

        svg = subprocess.check_output(["dot", "-Tsvg", f.name]).decode()
        svg = svg.replace('xlink:href=" "', "").replace('xlink:title="<TABLE>"', '')

        f.close()

        if self.outfile is not None:
            with open(self.outfile, 'w+') as f:
                f.write(dot_content)

        return svg

    def type_table(self, type):
        rows = header_fmt % (type.name, type.name, type.name)
        for idx, field in enumerate(type.fields):
            row_id = f"{type.name}_{idx}"
            type_name = field.type.name
            if type_name is None:
                type_name = str(field.type._type)
            text = f"{type_name}{field.prefix} {field.name}{field.suffix}"
            rows += row_fmt % (row_id, row_id, text)

        return table_fmt % (type.name, rows)
