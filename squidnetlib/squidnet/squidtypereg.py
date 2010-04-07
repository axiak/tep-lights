"""
SquidType register that houses all of the different types in a global dictionary.
"""

__all__ = ('squidtypes',)

class SquidTypeRegister(object):
    mapping = {}
    def register(self, *squidtypes):
        for squidtype in squidtypes:
            self.mapping[squidtype.clssquidtype()] = squidtype
squidtypes = SquidTypeRegister()

