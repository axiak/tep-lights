from squidnet.squidtypereg import squidtypes
from squidnet import sexp
from squidnet.combomethods import *

__aall__ = ('SquidBase64FileType',
           'SquidBooleanType',
           'SquidColorType',
           'SquidEnumType',
           'SquidIntegerType',
           'SquidRangeType',
           'SquidStringType',
           'SquidValue',
           'squidtypes',)


class SquidValue(object):
    value = None

    def __init__(self, value=None):
        self.value = value

    def __eq__(self, a):
        return self.squidtype == a.squidtype and self.value == a.value

    def __repr__(self):
        return '<%s: %s>' % (self.squidtype, self.value)

    __str__ = __unicode__ = __repr__

    @classmethod
    def clssquidtype(cls):
        return cls.__name__[5:-5].lower()

    @property
    def squidtype(self):
        return self.__class__.clssquidtype()

    @combomethod
    def get_sexp(cls, *args, **kwargs):
        if isinstance(cls, SquidValue):
            return cls.value_to_sexp()
        else:
            return cls.type_to_sexp(*args, **kwargs)

    @classmethod
    def type_to_sexp(cls, default=None):
        "Takes the given type and returns a "
        result = [sexp.Symbol(cls.clssquidtype())]
        if default is not None:
            result.extend([sexp.Symbol("default:"),
                           default.get_sexp()])
        return result

    def value_to_sexp(self):
        "Takes a value and tries to serialize it as a value of this type."
        if self.value is None:
            raise ValueError("Cannot be None Type")
        return self.value

    @classmethod
    def type_from_sexp(cls, sexpr):
        squidtype = squidtypes.mapping[str(sexpr)]
        return squidtype

    @classmethod
    def from_sexp(cls, sexpr):
        value = cls()
        value.read_sexp_value(sexpr)
        return value

    def sexp_value(self, s):
        """
        Takes an s-expression and tries to interpret it as a value of this
        type.
        """
        raise NotImplementedError("SquidValue: abstract class, can't unserialize value")



class SquidStringValue(SquidValue):
    def read_sexp_value(self, sexpr):
        self.value = sexpr
squidtypes.register(SquidStringValue)


class SquidIntegerValue(SquidValue):
    def read_sexp_value(self, sexpr):
        self.value = int(sexpr)
squidtypes.register(SquidIntegerValue)


class SquidRangeValue(SquidValue):
    def read_sexp_value(self, sexpr):
        self.value = float(sexpr)
squidtypes.register(SquidRangeValue)


class SquidBase64FileValue(SquidStringValue):
    pass
squidtypes.register(SquidBase64FileValue)


class SquidBooleanValue(SquidValue):
    def value_to_sexp(self):
        val = self.value
        return sexp.Symbol("t" if val else "f")

    def read_sexp_value(self, sexpr):
        self.value = False if sexpr==sexp.Symbol("f") else True
squidtypes.register(SquidBooleanValue)


class SquidColorValue(SquidValue):
    """
    A type that represents a Color type.
    Examples:

    >>> SquidColorValue((255, 0, 0)) # Red
    >>> SquidColorValue((255, 255, 255)) # White
    """
    def read_sexp_value(self, s):
        """
        Expected input: A list/tuple with strings or other int()-able object.
        Output: The self value will be updated to contain a nicely formatted tuple.
        """
        error = ValueError("Color expression must be a tuple of length 3")
        try:
            if len(s) != 3:
                raise error
        except ValueError:
            raise error
        value = tuple(int(s[i]) for i in range(3))
        for color in value:
            if color < 0 or color > 255:
                raise error
        self.value = value
squidtypes.register(SquidColorValue)


class SquidEnumValueBase(SquidValue):
    choices = []

    def __init__(self, value=None):
        value = str(value)
        self._validate(value)
        self.value = value

    @classmethod
    def clssquidtype(cls):
        return 'enum'

    @classmethod
    def type_to_sexp(cls, default=None):
        "Takes the given type and returns a "
        result = [[sexp.Symbol(cls.clssquidtype()),
                  sexp.Symbol('choices:'),
                  cls.choices]]
        
        if default is not None:
            result.extend([sexp.Symbol("default:"),
                           default.get_sexp()])
        return result

    def read_sexp_value(self, sexpr):
        sexpr = str(sexpr)
        self._validate(sexpr)
        self.value = sexpr

    def _validate(self, value):
        if value is None or value in self.choices:
            return
        raise ValueError("%s is not one of the valid choices: %r" % (value, self.choices))

def SquidEnumFactory(choices):
    return type('SquidEnumValue', (SquidEnumValueBase,),
                {'choices': list(map(str, choices))})
squidtypes.register(SquidEnumValueBase)

