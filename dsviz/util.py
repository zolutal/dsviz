import os

def print_gdb_type(type):
    print(type.name, "{")
    for field in type.fields():
        name = "" if field.name is None else field.name
        print("\t", field.type, name)
    print("}")

def read_module_file(name):
    f = open(os.path.join(os.path.dirname(__file__), name), 'r')
    content = f.read()
    f.close()
    return content

