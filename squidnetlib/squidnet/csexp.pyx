# sexp.py
# a library for handling (simplified) s-expressions
# doesn't bother with parsing data, but does bother with string delimiters

# main interface:
# read_all(string) -> list-based s-expressions
# write(s-exp list) -> string
# Symbol class to hold symbols (as opposed to strings)
# plist_find(p-list, key) -> elt (ignores first element)

__all__ = ('read_all', 'write', 'Symbol', 'plist_find',)

cdef class StringStream :
    cdef bytes str
    cdef int i
    def __init__(self, str) :
        self.str = str
        self.i = 0
    def read(self) :
        if self.i == len(self.str) :
            return ''
        else :
            self.i += 1
            return self.str[self.i-1]
    def peek(self) :
        if self.i == len(self.str) :
            return ''
        else :
            return self.str[self.i]

cdef class Symbol :
    cdef bytes s
    def __init__(self, s) :
        self.s = s
    def __richcmp__(Symbol self, Symbol s2, t) :
        if t == 2:
            return type(self) == type(s2) and self.s == s2.s
        elif t == 3:
            return type(self) != type(s2) or self.s != s2.s
        else:
            raise NotImplementedError("Invalid comparison: %s" % t)
    def __str__(self) :
        return self.s
    def __repr__(self) :
        return "<Symbol: %s>" % self.s

def plist_find(plist, key) :
    cdef int i
    for i in range(1, len(plist), 2) :
        if str(plist[i]) == str(key) :
            return plist[i+1]
    return None

def read_all(bytes str) :
    cdef StringStream stream
    stream = StringStream(str)
    ret = []
    while(stream.peek() != '') :
        r = read(stream)
        if r != None :
            ret.append(r)
    return ret

def read(StringStream stream) :
    sexp_eat_spaces(stream)
    if stream.peek() == '(' :
        stream.read()
        sexp_eat_spaces(stream)
        ret = []
        while stream.peek() != ')' :
            if stream.peek() == '' :
                raise Exception("Not enough closing paretheses")
            ret.append(read(stream))
            sexp_eat_spaces(stream)
        stream.read()
        return ret
    else :
        if stream.peek() == '"' :
            return sexp_read_string(stream)
        else :
            r = sexp_read_symbol(stream)
            try :
                return int(r)
            except ValueError :
                try :
                    return float(r)
                except ValueError :
                    return Symbol(r)

def sexp_read_string(stream) :
    stream.read()
    s = ""
    while True :
        if stream.peek() == '\\' :
            stream.read()
            e = stream.read()
            s += ("\\"+e).decode("string_escape")
        elif stream.peek() == '"' :
            stream.read()
            return s
        elif stream.peek() == '' :
            raise Exception("sexp_read_string: no closing quote")
        else :
            s += stream.read()

def sexp_read_symbol(stream) :
    r = stream.read()
    while not (sexp_is_whitespace(stream.peek())
               or stream.peek() == '('
               or stream.peek() == ')'
               or stream.peek() == '') :
        r += stream.read()
    return r

def one_of(thing, things) :
    for t in things :
        if thing == t :
            return True
    return False

def sexp_is_whitespace(a) :
    return one_of(a, [' ','\t','\n','\r','\f','\v'])

def sexp_eat_spaces(stream) :
    while(sexp_is_whitespace(stream.peek())) :
        stream.read()

def write(exp) :
    if isinstance(exp, list) :
        return "("+(" ".join([write(x) for x in exp]))+")"
    elif isinstance(exp, Symbol) :
        return str(exp)
    elif isinstance(exp, str) :
        return "\""+exp.encode("string_escape")+"\""
    else :
        return str(exp)
