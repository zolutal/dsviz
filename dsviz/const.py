graph_header = """
digraph structs {
    rankdir="LR"
    node [shape=plaintext];
    %s
}
"""
graph_node_fmt = "%s [label=%s];\n"
graph_edge_fmt = "%s -> %s;\n"


table_fmt = '<<TABLE Title="%s" Border="0" CellBorder="1" CellSpacing="0">%s</TABLE>>'

# HREF is a hack, see: https://stackoverflow.com/questions/48045987/assign-ids-to-td-elements-of-viz-js-to-appear-in-the-svg-elements
header_fmt = '<TR><TD ID="%s" HREF=" " PORT="%s" ALIGN="CENTER" BGCOLOR="gray"><b>%s</b></TD></TR>'
row_fmt = '<TR><TD ID="%s" HREF=" " PORT="%s" ALIGN="LEFT">%s</TD></TR>'


class TypeCode():
    TYPE_CODE_BITSTRING = -1
    TYPE_CODE_PTR = 1
    TYPE_CODE_ARRAY = 2
    TYPE_CODE_STRUCT = 3
    TYPE_CODE_UNION = 4
    TYPE_CODE_ENUM = 5
    TYPE_CODE_FLAGS = 6
    TYPE_CODE_FUNC = 7
    TYPE_CODE_INT = 8
    TYPE_CODE_FLT = 9
    TYPE_CODE_VOID = 10
    TYPE_CODE_SET = 11
    TYPE_CODE_RANGE = 12
    TYPE_CODE_STRING = 13
    TYPE_CODE_ERROR = 14
    TYPE_CODE_METHOD = 15
    TYPE_CODE_METHODPTR = 16
    TYPE_CODE_MEMBERPTR = 17
    TYPE_CODE_REF = 18
    TYPE_CODE_RVALUE_REF = 19
    TYPE_CODE_CHAR = 20
    TYPE_CODE_BOOL = 21
    TYPE_CODE_COMPLEX = 22
    TYPE_CODE_TYPEDEF = 23
    TYPE_CODE_NAMESPACE = 24
    TYPE_CODE_DECFLOAT = 25
    TYPE_CODE_INTERNAL_FUNCTION = 27
