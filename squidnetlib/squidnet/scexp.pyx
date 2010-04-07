cimport scsexp
from collections import deque
import sys

_Raise = object()

__all__ = ('SExpParseError', 'Symbol', 'read_all', 'write','plist_find','prettywrite',)

class SExpParseError(Exception):
    @staticmethod
    def from_code(code):
        return SExpParseError("Error parsing: %s (%d)" % (scsexp.SEXP_ERROR_DICT[code],
                                                          code))

cdef class Symbol:
    cdef unicode name
    def __cinit__(self, name):
        if isinstance(name, str):
            name = name.decode('utf8')
        self.name = name

    def __str__(self):
        return self.name.encode("utf8")
        
    def __repr__(self):
        return "sexp.Symbol(%r)" % self.name

    def __richcmp__(Symbol self, Symbol s2, t) :
        if t == 2:
            return type(self) == type(s2) and self.name == s2.name
        elif t == 3:
            return type(self) != type(s2) or self.name != s2.name
        else:
            raise NotImplementedError("Invalid comparison: %s" % t)

string_mapping = {
    "\\": "\\\\",
    "\n": "\\n",
    "\r": "\\r",
    "\"": "\\\"",
}

_full_mapping = {}

cdef _sexpr_repr(string):
    if isinstance(string, unicode):
        string = string.encode('utf8')
    if isinstance(string, basestring):
        if not _full_mapping:
            for i in range(256):
                _full_mapping[chr(i)] = string_mapping.get(chr(i), chr(i))
        return '"' + ''.join(map(_full_mapping.__getitem__, string)) + '"'
    else:
        return str(string)

def plist_find(plist, key, default=_Raise):
    key = str(key)
    for i in range(0, len(plist), 2):
        if str(plist[i]) == key:
            return plist[i + 1]
    if default is _Raise:
        raise KeyError("Could not find %s" % key)
    else:
        return default

def write(sexp):
    if not hasattr(sexp, '__iter__'):
        return _sexpr_repr(sexp)
    cdef list result = ['(']
    cdef int idx
    stack = deque([[sexp, 0]])
    while stack:
        sext, idx = stack[-1]
        if idx >= len(sext):
            result.append(')')
            stack.pop()
        else:
            sexp = sext[idx]
            stack[-1][1] += 1
            if idx:
                result.append(' ')

            if hasattr(sexp, '__iter__'):
                result.append('(')
                stack.append([sexp, 0])
            else:
                result.append(_sexpr_repr(sexp))
    return ''.join(result)

def prettywrite(sexp):
    indent = '    '
    if not hasattr(sexp, '__iter__'):
        return _sexpr_repr(sexp)
    cdef list result = ['(']
    cdef int idx
    stack = deque([[sexp, 0]])
    while stack:
        sext, idx = stack[-1]
        if idx >= len(sext):
            result.append(')')
            stack.pop()
        else:
            sexp = sext[idx]
            stack[-1][1] += 1
            if idx:
                result.append(' ')

            if hasattr(sexp, '__iter__'):
                result.append('\n' + len(stack) * indent + '(')
                stack.append([sexp, 0])
            else:
                result.append(_sexpr_repr(sexp))
    return ''.join(result)
    


def read_all(strdata):
    cdef scsexp.sexp_t *tdata
    cdef scsexp.sexp_t *fakehead
    cdef scsexp.sexp_t tmp
    cdef scsexp.pcont_t *cc = NULL
    cdef scsexp.faststack_t *stack
    cdef scsexp.stack_lvl_t *top
    cdef int depth = 0
    cdef scsexp.sexp_t *sx

    if isinstance(strdata, unicode):
        strdata = strdata.encode('utf8')

    strdata = '(' + strdata + ')'

    cc = scsexp.cparse_sexp(strdata, len(strdata), cc)
    sx = cc.last_sexp
    if cc.error != 0:
        error = SExpParseError.from_code(cc.error)
        if sx:
            scsexp.destroy_sexp(sx)
        scsexp.destroy_continuation(cc)
        raise error

    if sx == NULL:
        raise SExpParseError("Parsing failure: Unknown error")

    tmp = sx[0]
    tmp.next = tmp.list = NULL
    fakehead = scsexp.copy_sexp(&tmp)
    if fakehead == NULL:
        raise SExpParseError.from_code(1)
    fakehead.list = sx.list
    fakehead.next = NULL

    result = []
    lineage = deque([result])

    stack = scsexp.make_stack()
    scsexp.push(stack, fakehead)
    while stack.top != NULL:
        top = stack.top
        tdata = <scsexp.sexp_t *>top.data
        if tdata == NULL:
            scsexp.pop(stack)
            if stack.top == NULL:
                break
            lineage.pop()
            top = stack.top
            top.data = (<scsexp.sexp_t *>top.data).next
        elif tdata.ty == scsexp.SEXP_VALUE:
            if tdata.aty != scsexp.SEXP_BINARY and tdata.val_used > 0:
                curdata = tdata.val[:tdata.val_used - 1].decode('utf8')
                if tdata.aty == scsexp.SEXP_SQUOTE:
                    elem = u"'" + curdata
                elif tdata.aty == scsexp.SEXP_BASIC:
                    try:
                        elem = int(curdata)
                    except ValueError:
                        try:
                            elem = float(curdata)
                        except ValueError:
                            elem = Symbol(curdata)
                elif tdata.aty == scsexp.SEXP_DQUOTE:
                    elem = curdata
                lineage[-1].append(elem)
            top.data = <void *>((<scsexp.sexp_t*>top.data).next)
        elif tdata.ty == scsexp.SEXP_LIST:
            new_level = []
            lineage[-1].append(new_level)
            lineage.append(new_level)
            depth += 1
            scsexp.push(stack, tdata.list)
        else:
            raise SExpParseError.from_code(3)
    return result[0]
