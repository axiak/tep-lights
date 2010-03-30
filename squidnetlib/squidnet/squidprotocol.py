# squidprotocol.py
# an RPC system for SquidNet, a light, et cetera, controlling system.

import sexp

SQUIDNET_BROADCAST_PORT = 22222

class SquidServer(object) :
    def __init__(self, name, host, port, desc) :
        self.name = name if name is not None else ""
        self.host = host if host is not None else ""
        self.port = port if port is not None else 0
        self.desc = desc if desc is not None else ""
        self.devices = []
    def add_device(self, device) :
        self.devices.append(device)
        device.set_server(self)
    def get_device(self, name) :
        for device in self.devices :
            if device.name == name :
                return device
        return None
    def request(self, device, message, args={}) :
        d = self.get_device(device)
        if d is not None :
            return [sexp.Symbol("server-request"),
                    sexp.Symbol("name:"), self.name,
                    sexp.Symbol("host:"), self.host,
                    sexp.Symbol("port:"), self.port,
                    sexp.Symbol("request:"),
                    d.request(message, args)]
        else :
            raise Exception("No such device "+device)
    def handle(self, s) :
        """Takes an s-expression request and handles it, if the server can."""
        if s[0] == sexp.Symbol("server-request") :
            if (sexp.plist_find(s, sexp.Symbol("name:")) == self.name
                and sexp.plist_find(s, sexp.Symbol("host:")) == self.host
                and sexp.plist_find(s, sexp.Symbol("port:")) == self.port) :
                
                dr = sexp.plist_find(s, sexp.Symbol("request:"))
                drname = sexp.plist_find(dr, sexp.Symbol("name:"))
                d = self.get_device(drname)
                if d is not None :
                    return d.handle(dr)
                else :
                    raise Exception("Server has no device "+drname)
            else :
                raise Exception("Request not for this server")
        else :
            raise Exception("Not a server request")
    def get_sexp(self) :
        return [sexp.Symbol("server"),
                sexp.Symbol("name:"), self.name,
                sexp.Symbol("host:"), self.host,
                sexp.Symbol("port:"), self.port,
                sexp.Symbol("desc:"), self.desc,
                sexp.Symbol("devices:"),
                [x.get_sexp() for x in self.devices]]
    @staticmethod
    def load_sexp(s) :
        if s[0] == sexp.Symbol("server") :
            sv = SquidServer(sexp.plist_find(s, sexp.Symbol("name:")),
                             sexp.plist_find(s, sexp.Symbol("host:")),
                             sexp.plist_find(s, sexp.Symbol("port:")),
                             sexp.plist_find(s, sexp.Symbol("desc:")))
            ds = [SquidDevice.load_sexp(d)
                  for d in sexp.plist_find(s, sexp.Symbol("devices:")) or []]
            for d in ds :
                sv.add_device(d)
            return sv
        else :
            raise Exception("server: loading from incorrect s-expression")

class SquidDevice(object) :
    def __init__(self, name, desc) :
        self.name = name if name is not None else ""
        self.desc = desc if desc is not None else ""
        self.messages = []
    def __repr__(self):
        return '<SquidDevice %s>' % self.name
    def add_message(self, message) :
        self.messages.append(message)
        message.set_device(self)
    def get_message(self, name) :
        for message in self.messages :
            if message.name == name :
                return message
        return None
    def set_server(self, server) :
        self.server = server
    def request(self, message, args={}) :
        m = self.get_message(message)
        if m is not None :
            return [sexp.Symbol("device-request"),
                    sexp.Symbol("name:"),self.name,
                    sexp.Symbol("request:"),m.request(args)]
        else :
            raise Exception("No such message "+message)
    def handle(self, s) :
        if s[0] == sexp.Symbol("device-request") :
            if self.name == sexp.plist_find(s, sexp.Symbol("name:")) :
                r = sexp.plist_find(s, sexp.Symbol("request:"))
                rname = sexp.plist_find(r, sexp.Symbol("name:"))
                m = self.get_message(rname)
                if m is not None :
                    return m.handle(r)
                else :
                    raise Exception("No such message "+rname)
            else :
                raise Exception("Device request not for this device")
        else :
            raise Exception("Not a device request")
    def get_sexp(self) :
        return [sexp.Symbol("device"),
                sexp.Symbol("name:"), self.name,
                sexp.Symbol("desc:"), self.desc,
                sexp.Symbol("messages:"),
                [x.get_sexp() for x in self.messages]]
    @staticmethod
    def load_sexp(s) :
        if s[0] == sexp.Symbol("device") :
            d = SquidDevice(sexp.plist_find(s, sexp.Symbol("name:")),
                            sexp.plist_find(s, sexp.Symbol("desc:")))
            ms = [SquidMessage.load_sexp(m)
                  for m in sexp.plist_find(s, sexp.Symbol("messages:")) or []]
            for m in ms :
                d.add_message(m)
            return d
        else :
            raise Exception("device: loading from incorrect s-expression")

class SquidMessage(object):
    def __init__(self, name, desc, arguments, handler=None) :
        self.name = name if name is not None else ""
        self.desc = desc if desc is not None else ""
        self.arguments = arguments or []
        self.handler = handler

    def __repr__(self):
        return '<SquidMessage: %s>' % (self.name)

    def set_device(self, device) :
        self.device = device
    def set_handler(self, function) :
        """Set's the handler to a one-argument function which takes a
        dictionary of String/SquidValue pairs"""
        self.handler = function
    def get_argument(self, name) :
        for a in self.arguments :
            if a.name == name :
                return a
        return None
    def request(self, args={}) :
        """Creates a message request where args is a dictionary of
        name/SquidValue pairs"""
        args2 = [a.request(args) for a in self.arguments]
        return [sexp.Symbol("message-request"),
                sexp.Symbol("name:"), self.name,
                sexp.Symbol("arguments:"), args2]
    def handle(self, s) :
        if self.handler is not None :
            if s[0] == sexp.Symbol("message-request") :
                if sexp.plist_find(s, sexp.Symbol("name:")) == self.name :
                    args = self.decode_sexp_args(sexp.plist_find(s, sexp.Symbol("arguments:")))
                    self.handler(args)
                else :
                    raise Exception("Message request not this message type")
            else :
                raise Exception("Not a message request")
        else :
            raise Exception("Message \""+self.name+"\" has no handler")
    def decode_sexp_args(self, arglist) :
        args = {}
        for a in self.arguments or [] :
            args[a.name] = a.handle(arglist)
        return args
    def get_sexp(self) :
        return [sexp.Symbol("message"),
                sexp.Symbol("name:"), self.name,
                sexp.Symbol("desc:"), self.desc,
                sexp.Symbol("arguments:"),
                [x.get_sexp() for x in self.arguments]]
    @staticmethod
    def load_sexp(s) :
        if s[0] == sexp.Symbol("message") :
            ars = [SquidArgument.load_sexp(a)
                  for a in sexp.plist_find(s, sexp.Symbol("arguments:")) or []]
            m = SquidMessage(sexp.plist_find(s, sexp.Symbol("name:")),
                             sexp.plist_find(s, sexp.Symbol("desc:")),
                             ars)
            return m
        else :
            raise Exception("message: loading from incorrect s-expression")

class SquidArgument :
    def __init__(self, name, argtype, default=None) :
        self.name = name if name is not None else ""
        self.argtype = argtype if argtype is not None else ""
        self.default = default
    def request(self, args) :
        """args is a list of name/SquidValue pairs, and the SquidArgument
        tries to find its argument."""
        if self.name in args :
            return [sexp.Symbol(str(self.name)), args[self.name].get_sexp()]
        else :
            if self.default is not None :
                return [self.name, self.default.get_sexp()]
            else :
                raise Exception("Argument "+self.name+" not satisfied")
    def handle(self, argslist) :
        for arg in argslist :
            if str(arg[0]) == self.name :
                return self.argtype.read_sexp_value(arg[1])
        if self.default is not None :
            return self.default
        else :
            raise Exception("Missing argument "+self.name)
    def get_sexp(self) :
        r = [sexp.Symbol("argument"),
             sexp.Symbol("name:"), self.name,
             sexp.Symbol("type:"), self.argtype.get_sexp()]
        if self.default is not None :
            r.append(sexp.Symbol("default:"))
            r.append(self.default.get_sexp())
        return r
    @staticmethod
    def load_sexp(s) :
        if s[0] == sexp.Symbol("argument") :
            argtype = SquidType.load_sexp(sexp.plist_find(s, sexp.Symbol("type:")))
            default = sexp.plist_find(s, sexp.Symbol("default:"))
            if default is not None :
                default = argtype.read_sexp_value(default)
            m = SquidArgument(sexp.plist_find(s, sexp.Symbol("name:")),
                              argtype,
                              default)
            return m
        else :
            raise Exception("argument: loading from incorrect s-expression")

class SquidTypeRegister(object):
    mapping = {}
    def register(self, *squidtypes):
        for squidtype in squidtypes:
            self.mapping[squidtype.argtype] = squidtype
squidtypes = SquidTypeRegister()

class SquidType(object):
    argtype = ""
    def __init__(self, argtype = None) :
        if argtype:
            self.argtype = argtype
    def __eq__(self, a) :
        return self.argtype == a.argtype
    def __str__(self) :
        return self.argtype
    def get_sexp(self) :
        return sexp.Symbol(self.argtype)
    @staticmethod
    def load_sexp(s) :
        if isinstance(s,list) :
            return SquidEnumType.load_sexp(s)
        t = str(s)
        try:
            return squidtypes.mapping[t]()
        except KeyError:
            raise KeyError("SquidType: Unknown type %s" % t)
    def value_to_sexp(self, val) :
        """Takes a value and tries to serialize it as a value of this type."""
        raise Exception("SquidType: abstract class, can't serialize value")
    def read_sexp_value(self, s) :
        """Takes an s-expression and tries to interpret it as a value of this
        type."""
        raise Exception("SquidType: abstract class, can't unserialize value")

class SquidValue(object):
    argtype = ""
    def __init__(self, argtype, value) :
        self.argtype = argtype
        self.value = value
    def get_sexp(self) :
        return self.argtype.value_to_sexp(self.value)

class SquidIntegerType(SquidType) :
    argtype = "integer"
    def value_to_sexp(self, val) :
        return int(val)
    def read_sexp_value(self, s) :
        return SquidValue(self, int(s))

squidtypes.register(SquidIntegerType)

class SquidRangeType(SquidType) :
    argtype = "range"
    def value_to_sexp(self, val) :
        return float(val)
    def read_sexp_value(self, s) :
        return SquidValue(self, float(s))

squidtypes.register(SquidRangeType)

class SquidColorType(SquidType) :
    argtype = "color"
    def value_to_sexp(self, val) :
        return [int(val[0]), int(val[1]), int(val[2])]
    def read_sexp_value(self, s) :
        r = int(s[0])
        g = int(s[1])
        b = int(s[2])
        return SquidValue(self, [r,g,b])

squidtypes.register(SquidColorType)

class SquidStringType(SquidType) :
    argtype = "string"
    def value_to_sexp(self, val) :
        return str(val)
    def read_sexp_value(self, s) :
        return SquidValue(self, str(s))

squidtypes.register(SquidStringType)

class SquidBase64FileType(SquidType):
    argtype = 'base64file'
    def value_to_sexp(self, val):
        return val
    def read_sexp_value(self, s):
        return SquidValue(self, s)

squidtypes.register(SquidBase64FileType)

class SquidBooleanType(SquidType) :
    argtype = "boolean"
    def value_to_sexp(self, val) :
        return sexp.Symbol("t" if val else "f")
    def read_sexp_value(self, s) :
        return SquidValue(self, False if s==sexp.Symbol("f") else True)

squidtypes.register(SquidBooleanType)

class SquidEnumType(SquidType) :
    def __init__(self, argtype, options) :
        self.argtype = argtype
        self.options = options
    @staticmethod
    def get_sexp(self) :
        s = [sexp.Symbol(self.argtype)]
        s.extend(self.options)
        return s
    def load_sexp(s) :
        return SquidEnumType(s[0], s[1:])
    def value_to_sexp(self, val) :
        return val
    def read_sexp_value(self, s) :
        if s in self.options :
            return SquidValue(self, s)
        else :
            return "Enum error: can't have \"%s\"" % s

squidtypes.register(SquidEnumType)

if __name__=="__main__" :
    def test_handler(args) :
        print "Got args: "+str(args)
    s = SquidServer("kmill", "kmill.mit.edu", 2222, "Kyle's computer")
    d1 = SquidDevice("22-lights", "The lights in 22")
    s.add_device(d1)
    d1.add_message(SquidMessage("set",
                                "Set the lights to a color",
                                [SquidArgument("color", SquidColorType(),
                                               SquidValue(SquidColorType(), [25, 25, 25]))],
                                test_handler))
    d1.add_message(SquidMessage("stop",
                                "Stops the lights",
                                []))
    
    print sexp.write(s.get_sexp())
    print
    print sexp.write(SquidServer.load_sexp(sexp.read_all(sexp.write(s.get_sexp()))[0]).get_sexp())
    print
    print sexp.write(s.request("22-lights", "set"))
    print
    print s.handle(s.request("22-lights", "set"))
