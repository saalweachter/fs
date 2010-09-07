"""
XDR implementation, using xdrlib for packing.
"""

import xdrlib as _xdr


class XDRBadValue(object):
    pass


class _xdr_type(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        class member_table(dict):
            def __init__(self):
                self.member_names = []

            def __setitem__(self, key, value):
                if key not in self:
                    self.member_names.append(key)
                dict.__setitem__(self, key, value)

        return member_table()

    def __new__(cls, name, bases, classdict):
        result = type.__new__(cls, name, bases, dict(classdict))
        result.member_names = classdict.member_names
        return result

class xdr_object(object, metaclass=_xdr_type):
    pass


class xdr_void(xdr_object):
    def pack(self, packer):
        pass

    @staticmethod
    def unpack(unpacker):
        return xdr_void()


class xdr_int(xdr_object):
    def __init__(self, value):
        if type(value) is not int:
            raise XDRBadValue
        if value >= 2**31:
            raise XDRBadValue
        if value < -2**31:
            raise XDRBadValue
        self.value = value

    def __eq__(self, value):
        return value == self.value

    def __int__(self):
        return self.value

    def __hash__(self):
        return self.value.__hash__()

    def pack(self, packer):
        packer.pack_int(self.value)

    @staticmethod
    def unpack(unpacker):
        value = unpacker.unpack_int()
        return xdr_int(value)

class xdr_uint(xdr_object):
    def __init__(self, value):
        if type(value) is not int:
            raise XDRBadValue
        if value >= 2**32:
            raise XDRBadValue
        if value < 0:
            raise XDRBadValue
        self.value = value

    def __eq__(self, value):
        return value == self.value

    def __int__(self):
        return self.value

    def __hash__(self):
        return self.value.__hash__()

    def pack(self, packer):
        packer.pack_uint(self.value)

    @staticmethod
    def unpack(unpacker):
        value = unpacker.unpack_uint()
        return xdr_uint(value)

class xdr_enum(xdr_object):
    def __init__(self, value):
        for k, v in self.values():
            if v == value:
                break
        else:
            raise XDRBadValue
        self.value = value

    def __eq__(self, value):
        return value == self.value

    def __int__(self):
        return self.value

    def __hash__(self):
        return self.value.__hash__()

    @classmethod
    def values(cls):
        return [ (k, v)
                 for k, v in cls.__dict__.items()
                 if type(v) is int ]

    def pack(self, packer):
        packer.pack_enum(self.value)

    @classmethod
    def unpack(kls, unpacker):
        value = unpacker.unpack_enum()
        return kls(value)

class xdr_bool(xdr_object):
    def __init__(self, value):
        if type(value) is not bool:
            raise XDRBadValue
        self.value = value

    def __eq__(self, value):
        return value == self.value

    def __bool__(self):
        return self.value

    @classmethod
    def values(cls):
        return [ ("FALSE", 0), ("TRUE", 1) ]

    def pack(self, packer):
        packer.pack_bool(self.value)

    @staticmethod
    def unpack(unpacker):
        value = unpacker.unpack_bool()
        return xdr_bool(value)

class xdr_hyper(xdr_object):
    def __init__(self, value):
        if type(value) is not int:
            raise XDRBadValue
        if value >= 2**63:
            raise XDRBadValue
        if value < -2**63:
            raise XDRBadValue
        self.value = value

    def __eq__(self, value):
        return value == self.value

    def __int__(self):
        return self.value

    def __hash__(self):
        return self.value.__hash__()

    def pack(self, packer):
        packer.pack_hyper(self.value)

    @staticmethod
    def unpack(unpacker):
        value = unpacker.unpack_hyper()
        return xdr_hyper(value)

class xdr_uhyper(xdr_object):
    def __init__(self, value):
        if type(value) is not int:
            raise XDRBadValue
        if value >= 2**64:
            raise XDRBadValue
        if value < 0:
            raise XDRBadValue
        self.value = value

    def __eq__(self, value):
        return value == self.value

    def __int__(self):
        return self.value

    def __hash__(self):
        return self.value.__hash__()

    def pack(self, packer):
        packer.pack_uhyper(self.value)

    @staticmethod
    def unpack(unpacker):
        value = unpacker.unpack_uhyper()
        return xdr_uhyper(value)

class xdr_float(xdr_object):
    def __init__(self, value):
        if type(value) is not float:
            raise XDRBadValue
        self.value = value

    def __eq__(self, value):
        return value == self.value

    def __float__(self):
        return self.value

    def pack(self, packer):
        packer.pack_float(self.value)

    @staticmethod
    def unpack(unpacker):
        value = unpacker.unpack_float()
        return xdr_float(value)

class xdr_double(xdr_object):
    def __init__(self, value):
        if type(value) is not float:
            raise XDRBadValue
        self.value = value

    def __eq__(self, value):
        return value == self.value

    def __float__(self):
        return self.value

    def pack(self, packer):
        packer.pack_double(self.value)

    @staticmethod
    def unpack(unpacker):
        value = unpacker.unpack_double()
        return xdr_double(value)

class xdr_quad(xdr_object):
    def __init__(self, value):
        if type(value) is not float:
            raise XDRBadValue
        self.value = value

    def __eq__(self, value):
        return value == self.value

    def __float__(self):
        return self.value

    def pack(self, packer):
        packer.pack_quad(self.value)

    @staticmethod
    def unpack(unpacker):
        value = unpacker.unpack_quad()
        return xdr_quad(value)

def xdr_opaque(max=None, size=None):
    if max == None and size == None:
        max = 2**32-1
    if size:
        max = size
    class _xdr_opaque(xdr_object):
        def __init__(self, _bytes):
            if not isinstance(_bytes, bytes):
                raise XDRBadValue
            if self.__class__.max:
                if len(_bytes) > self.__class__.max:
                    raise XDRBadValue
            self.bytes = _bytes

        def pack(self, packer):
            if "size" in self.__class__.__dict__:
                packer.pack_fopaque(self.__class__.size, self.bytes)
            else:
                packer.pack_opaque(self.bytes)

        @classmethod
        def unpack(kls, unpacker):
            if "size" in kls.__dict__:
                bytes = unpacker.unpack_fopaque(kls.size)
            else:
                bytes = unpacker.unpack_opaque()
            return kls(bytes)

    _xdr_opaque.max = max
    if size:
        _xdr_opaque.size = size
    return _xdr_opaque

def xdr_string(max=None):
    if max == None:
        max = 2**32-1
    class _xdr_string(xdr_object):
        def __init__(self, _bytes):
            if type(_bytes) is str:
                _bytes = _bytes.encode("utf8")
            if type(_bytes) is not bytes:
                raise XDRBadValue
            if self.__class__.max:
                if len(_bytes) > self.__class__.max:
                    raise XDRBadValue
            self.bytes = _bytes

        def __str__(self):
            return self.bytes.decode("utf8")

        def __hash__(self):
            return self.bytes.__hash__()

        def pack(self, packer):
            packer.pack_string(self.bytes)

        @classmethod
        def unpack(kls, unpacker):
            bytes = unpacker.unpack_string()
            return kls(bytes)

    _xdr_string.max = max
    return _xdr_string

class xdr_struct(xdr_object):
    def __init__(self, **kwds):
        members = self.members()
        members_dict = dict(members)
        for k, v in kwds.items():
            if k not in members_dict:
                raise XDRBadValue
            if not isinstance(v, members_dict[k]):
                v = members_dict[k](v)
            self.__dict__[k] = v
        for k, v in members:
            if k not in self.__dict__:
                raise XDRBadValue

    def members(self):
        return [ (k, v)
                 for k, v in self.__class__.__dict__.items()
                 if isinstance(v, type) ]

    def pack(self, packer):
        for k in self.__class__.member_names:
            if isinstance(self.__getattribute__(k), xdr_object):
                self.__getattribute__(k).pack(packer)

    @classmethod
    def unpack(cls, unpacker):
        d = {}
        for k in cls.member_names:
            if isinstance(cls.__dict__[k], type):
                v = cls.__dict__[k].unpack(unpacker)
                d[k] = v
        return cls(**d)



def xdr_union(**kwd):
    if len(kwd) != 1:
        raise XDRBadValue
    key, value = list(kwd.items())[0]
    class _xdr_case(xdr_object):
        def __init__(self):
            xdr_object.__setattr__(self, "member_names", [])
        def __setattr__(self, key, value):
            if key not in self.member_names:
                self.member_names.append(key)
            xdr_object.__setattr__(self, key, value)
    class _xdr_union_type(_xdr_type):
        @classmethod
        def __prepare__(metacls, name, bases):
            d = {}
            d[key] = value
            for k, v in value.values():
                d[k] = _xdr_case()
            return d

        def __new__(cls, name, bases, classdict):
            result = type.__new__(cls, name, bases, classdict)
            return result

    class _xdr_union(xdr_object, metaclass=_xdr_union_type):
        def __init__(self, **kwds):
            if key not in kwds:
                raise XDRBadValue
            if isinstance(kwds[key], xdr_object):
                xdr_value = kwds[key]
                raw_value = xdr_value.value
            else:
                raw_value = kwds[key]
                xdr_value = value(raw_value)
            self.__setattr__(key, xdr_value)
            self.member_names = []
            self.member_names.append(key)
            for k, v in value.values():
                if raw_value == v:
                    branch = k
                    break
            else:
                raise XDRBadValue
            implied = self.__class__.__dict__[branch]
            for m in implied.member_names:
                if m not in kwds:
                    raise XDRBadValue
                v = kwds[m]
                if not isinstance(v, implied.__getattribute__(m)):
                    v = implied.__getattribute__(m)(v)
                self.__setattr__(m, v)
                self.member_names.append(m)

        def pack(self, packer):
            for name in self.member_names:
                v = self.__getattribute__(name)
                v.pack(packer)

        @classmethod
        def unpack(cls, unpacker):
            branch_value = value.unpack(unpacker)
            for k, v in value.values():
                if v == branch_value.value:
                    branch = k
                    break
            else:
                raise XDRBadValue
            d = {}
            d[key] = branch_value
            case = cls.__dict__[branch]
            if not case:
                raise XDRBadValue
            for k in case.member_names:
                v = case.__getattribute__(k).unpack(unpacker)
                d[k] = v
            return cls(**d)

    return _xdr_union


def xdr_array(element_type, max=None, size=None):
    if max == None and size == None:
        max = 2**32-1
    if size:
        max = size
    class _xdr_array(xdr_object):
        def __init__(self, *elements):
            if size is not None:
                if len(elements) != size:
                    raise XDRBadValue
            self.elements = [ e if isinstance(e, element_type)
                              else element_type(e)
                              for e in elements ]

        def __index__(self, n):
            return self.elements[n]

        def pack(self, packer):
            if size is None:
                packer.pack_uint(len(self.elements))
            for e in self.elements:
                e.pack(packer)

        @classmethod
        def unpack(cls, unpacker):
            if size is None:
                sz = unpacker.unpack_uint()
            else:
                sz = size
            elems = [ element_type.unpack(unpacker)
                      for i in range(sz) ]
            return cls(elems)

    _xdr_array.element_type = element_type
    _xdr_array.max = max
    if size is not None:
        _xdr_array.size = size

    return _xdr_array


def xdr_optional(element_type):
    return xdr_array(element_type, max=1)


if __name__ == "__main__":

    bananas = xdr_array(xdr_uint)
    apples = bananas(1, 2, 3, 4)
    packer = _xdr.Packer()
    apples.pack(packer)
    print(packer.get_buffer())
