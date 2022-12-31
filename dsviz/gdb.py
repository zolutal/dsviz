from rpyc.utils.factory import unix_connect
from dsviz.types import Struct
import subprocess
import tempfile
import pathlib
import time
import os

class Gdb:
    def __init__(self):
        self.api = self.start_server()

    def add_symbol_file(self, sym_path: str):
        path = pathlib.Path(sym_path)
        if not path.exists():
            raise Exception("Specified path does not exist")
        self.api.execute(f"add-symbol-file {path}")

    def lookup_type(self, type_name: str):
        return self.api.lookup_type(type_name)

    def find_struct(self, struct_name: str):
        type = self.lookup_type(struct_name)
        if type.code != self.api.TYPE_CODE_STRUCT:
            print("found type was not a struct, code:", type.code)
        return Struct(type)

    def api_bridge_path(self):
        bridge_path = os.path.join(os.path.dirname(__file__), 'gdb_api_bridge.py')
        return bridge_path

    def start_server(self):
        """
        Credit: pwntools; Copyright (c) 2015 Gallopsled et al.
        Starts a gdb api pyrc server
        """
        socket_dir = tempfile.mkdtemp()
        socket_path = os.path.join(socket_dir, 'socket')
        bridge = self.api_bridge_path()

        gdbscript = f"python socket_path = '{socket_path}'; time.sleep(1)\nsource {bridge}"
        tmp = tempfile.NamedTemporaryFile(prefix = 'dsv', suffix = '.gdb',
                                              delete = False, mode = 'w+')
        gdbscript = 'shell rm %s\n%s' % (tmp.name, gdbscript)
        tmp.write(gdbscript)
        tmp.close()

        cmd = ("gdb", "-x", tmp.name)
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # wait for the server to start
        conn = None
        start = time.time()
        while (time.time() - start < 10):
            try:
                conn = unix_connect(socket_path)
                break
            except Exception as e:
                time.sleep(0.1)

        # clean up socket file
        os.unlink(socket_path)
        os.rmdir(socket_dir)

        if conn is None:
            raise Exception("Failed to connect to socket")

        gdb = conn.root.exposed_gdb
        return gdb
