from dsviz.const import TypeCode
import uuid

class Type:
    def __init__(self, type, deref_ct=0, parent=None):
        # graphviz doesn't like node names starting with numbers, so prepending 'id'
        self.id = 'id' + uuid.uuid4().hex
        self._type = type.strip_typedefs()
        for _ in range(deref_ct):
            self._type = self._type.target()
        self._parent = parent
        self.name = self._type.name
        self.fields = []

    def init_fields(self):
        pass

class Struct(Type):
    def __init__(self, type, deref_ct=0, parent=None):
        super().__init__(type, deref_ct, parent)
        if self.name is None:
            self.name = "struct"

    def init_fields(self):
        for field in self._type.fields():
            self.fields.append(Field(field, self))

class Union(Type):
    def __init__(self, type, parent=None):
        super().__init__(type, 0, parent)
        self.name = 'union'
        self.fields = []

    def init_fields(self):
        for field in self._type.fields():
            self.fields.append(Field(field, self))

class Field:
    def __init__(self, field, parent):
        self._field = field
        self._parent = parent
        self.name = field.name if field.name is not None else ""
        self.ptr = False
        self.deref_ct = 0
        self.prefix = ""
        self.suffix = ""

        cur_type = field.type.strip_typedefs()
        deref_ct = 0
        while cur_type.code in (TypeCode.TYPE_CODE_PTR, TypeCode.TYPE_CODE_ARRAY): # deref ptr and array
            if cur_type.code == TypeCode.TYPE_CODE_PTR:
                self.prefix += "*"
            if cur_type.code == TypeCode.TYPE_CODE_ARRAY:
                self.suffix += f"[{cur_type.sizeof//cur_type.target().sizeof}]"
            cur_type = cur_type.target().strip_typedefs()
            deref_ct += 1

        self.code = cur_type.code
        self.deref_ct = deref_ct

        print(self.name, self.code)

        match self.code:
            case TypeCode.TYPE_CODE_STRUCT:
                self.type = Struct(self._field.type, deref_ct, self)
            case TypeCode.TYPE_CODE_UNION :
                self.type = Union(self._field.type, self)
            case _:
                self.type = Type(self._field.type, deref_ct, self)

