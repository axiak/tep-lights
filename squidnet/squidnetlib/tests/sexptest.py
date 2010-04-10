from squidnet import scexp as sexp
import functools
import gc
import time

def read_all(s):
    """
    >>> read_all('(server name: "kmill" host: "kmill.mit.edu" port: 2222 desc: "Kyle\\\'s computer" devices: ((device name: "22-lights" desc: "The lights in 22" messages: ((message name: "cycle" desc: "Cycle the lights" arguments: ()) (message name: "set" desc: "Set the color of the lights" arguments: ((argument name: "color" type: color))) (message name: "stop" desc: "Stops the lights" arguments: ()))) (device name: "stairwell" desc: "The stairwell lights" messages: ((message name: "cycle" desc: "Cycle the lights" arguments: ()) (message name: "set-floor2" desc: "Set the color of the second landing" arguments: ((argument name: "color" type: color))) (message name: "set-floor3" desc: "Set the color of the third landing" arguments: ((argument name: "color" type: color))) (message name: "set-floor4" desc: "Set the color of the fourth landing" arguments: ((argument name: "color" type: color))) (message name: "set" desc: "Set the color of the stairwell" arguments: ((argument name: "color" type: color))) (message name: "stop" desc: "Stop the lights" arguments: ()))) (device name: "computer" desc: "Kyle\\\'s computer" messages: ((message name: "say" desc: "Says a phrase" arguments: ((argument name: "text" type: string)))))))')
    [[<Symbol: server>, <Symbol: name:>, u'kmill', <Symbol: host:>, u'kmill.mit.edu', <Symbol: port:>, 2222, <Symbol: desc:>, "Kyle's computer", <Symbol: devices:>, [[<Symbol: device>, <Symbol: name:>, u'22-lights', <Symbol: desc:>, u'The lights in 22', <Symbol: messages:>, [[<Symbol: message>, <Symbol: name:>, u'cycle', <Symbol: desc:>, u'Cycle the lights', <Symbol: arguments:>, []], [<Symbol: message>, <Symbol: name:>, u'set', <Symbol: desc:>, u'Set the color of the lights', <Symbol: arguments:>, [[<Symbol: argument>, <Symbol: name:>, u'color', <Symbol: type:>, <Symbol: color>]]], [<Symbol: message>, <Symbol: name:>, u'stop', <Symbol: desc:>, u'Stops the lights', <Symbol: arguments:>, []]]], [<Symbol: device>, <Symbol: name:>, u'stairwell', <Symbol: desc:>, u'The stairwell lights', <Symbol: messages:>, [[<Symbol: message>, <Symbol: name:>, u'cycle', <Symbol: desc:>, u'Cycle the lights', <Symbol: arguments:>, []], [<Symbol: message>, <Symbol: name:>, u'set-floor2', <Symbol: desc:>, u'Set the color of the second landing', <Symbol: arguments:>, [[<Symbol: argument>, <Symbol: name:>, u'color', <Symbol: type:>, <Symbol: color>]]], [<Symbol: message>, <Symbol: name:>, u'set-floor3', <Symbol: desc:>, u'Set the color of the third landing', <Symbol: arguments:>, [[<Symbol: argument>, <Symbol: name:>, u'color', <Symbol: type:>, <Symbol: color>]]], [<Symbol: message>, <Symbol: name:>, u'set-floor4', <Symbol: desc:>, u'Set the color of the fourth landing', <Symbol: arguments:>, [[<Symbol: argument>, <Symbol: name:>, u'color', <Symbol: type:>, <Symbol: color>]]], [<Symbol: message>, <Symbol: name:>, u'set', <Symbol: desc:>, u'Set the color of the stairwell', <Symbol: arguments:>, [[<Symbol: argument>, <Symbol: name:>, u'color', <Symbol: type:>, <Symbol: color>]]], [<Symbol: message>, <Symbol: name:>, u'stop', <Symbol: desc:>, u'Stop the lights', <Symbol: arguments:>, []]]], [<Symbol: device>, <Symbol: name:>, u'computer', <Symbol: desc:>, "Kyle's computer", <Symbol: messages:>, [[<Symbol: message>, <Symbol: name:>, u'say', <Symbol: desc:>, u'Says a phrase', <Symbol: arguments:>, [[<Symbol: argument>, <Symbol: name:>, u'text', <Symbol: type:>, <Symbol: string>]]]]]]]]
"""
    return sexp.read_all(s)


data =  '(server name: "kmill" host: "kmill.mit.edu" port: 2222 desc: "Kyle\\\'s computer" devices: ((device name: "22-lights" desc: "The lights in 22" messages: ((message name: "cycle" desc: "Cycle the lights" arguments: ()) (message name: "set" desc: "Set the color of the lights" arguments: ((argument name: "color" type: color))) (message name: "stop" desc: "Stops the lights" arguments: ()))) (device name: "stairwell" desc: "The stairwell lights" messages: ((message name: "cycle" desc: "Cycle the lights" arguments: ()) (message name: "set-floor2" desc: "Set the color of the second landing" arguments: ((argument name: "color" type: color))) (message name: "set-floor3" desc: "Set the color of the third landing" arguments: ((argument name: "color" type: color))) (message name: "set-floor4" desc: "Set the color of the fourth landing" arguments: ((argument name: "color" type: color))) (message name: "set" desc: "Set the color of the stairwell" arguments: ((argument name: "color" type: color))) (message name: "stop" desc: "Stop the lights" arguments: ()))) (device name: "computer" desc: "Kyle\\\'s computer" messages: ((message name: "say" desc: "Says a phrase" arguments: ((argument name: "text" type: string)))))))'

sexp_data = [sexp.Symbol('server'),
             sexp.Symbol('name:'),
             'kmill',
             sexp.Symbol('host:'),
             'kmill.mit.edu',
             sexp.Symbol('port:'),
             2222,
             sexp.Symbol('desc:'),
             "Kyle's computer",
             sexp.Symbol('devices:'),
             [[sexp.Symbol('device'),
               sexp.Symbol('name:'),
               '22-lights',
               sexp.Symbol('desc:'),
               'The lights in 22',
               sexp.Symbol('messages:'),
               [[sexp.Symbol('message'),
                 sexp.Symbol('name:'),
                 'cycle',
                 sexp.Symbol('desc:'),
                 'Cycle the lights',
                 sexp.Symbol('arguments:'),
                 []],
                [sexp.Symbol('message'),
                 sexp.Symbol('name:'),
                 'set',
                 sexp.Symbol('desc:'),
                 'Set the color of the lights',
                 sexp.Symbol('arguments:'),
                 [[sexp.Symbol('argument'),
                   sexp.Symbol('name:'),
                   'color',
                   sexp.Symbol('type:'),
                   sexp.Symbol('color')]]],
                [sexp.Symbol('message'),
                 sexp.Symbol('name:'),
                 'stop',
                 sexp.Symbol('desc:'),
                 'Stops the lights',
                 sexp.Symbol('arguments:'),
                 []]]],
              [sexp.Symbol('device'),
               sexp.Symbol('name:'),
               'stairwell',
               sexp.Symbol('desc:'),
               'The stairwell lights',
               sexp.Symbol('messages:'),
               [[sexp.Symbol('message'),
                 sexp.Symbol('name:'),
                 'cycle',
                 sexp.Symbol('desc:'),
                 'Cycle the lights',
                 sexp.Symbol('arguments:'),
                 []],
                [sexp.Symbol('message'),
                 sexp.Symbol('name:'),
                 'set-floor2',
                 sexp.Symbol('desc:'),
                 'Set the color of the second landing',
                 sexp.Symbol('arguments:'),
                 [[sexp.Symbol('argument'),
                   sexp.Symbol('name:'),
                   'color',
                   sexp.Symbol('type:'),
                   sexp.Symbol('color')]]],
                [sexp.Symbol('message'),
                 sexp.Symbol('name:'),
                 'set-floor3',
                 sexp.Symbol('desc:'),
                 'Set the color of the third landing',
                 sexp.Symbol('arguments:'),
                 [[sexp.Symbol('argument'),
                   sexp.Symbol('name:'),
                   'color',
                   sexp.Symbol('type:'),
                   sexp.Symbol('color')]]],
                [sexp.Symbol('message'),
                 sexp.Symbol('name:'),
                 'set-floor4',
                 sexp.Symbol('desc:'),
                 'Set the color of the fourth landing',
                 sexp.Symbol('arguments:'),
                 [[sexp.Symbol('argument'),
                   sexp.Symbol('name:'),
                   'color',
                   sexp.Symbol('type:'),
                   sexp.Symbol('color')]]],
                [sexp.Symbol('message'),
                 sexp.Symbol('name:'),
                 'set',
                 sexp.Symbol('desc:'),
                 'Set the color" of the stairwell',
                 sexp.Symbol('arguments:'),
                 [[sexp.Symbol('argument'),
                   sexp.Symbol('name:'),
                   'color',
                   sexp.Symbol('type:'),
                   sexp.Symbol('color')]]],
                [sexp.Symbol('message'),
                 sexp.Symbol('name:'),
                 'stop',
                 sexp.Symbol('desc:'),
                 'Stop the lights',
                 sexp.Symbol('arguments:'),
                 []]]],
              [sexp.Symbol('device'),
               sexp.Symbol('name:'),
               'computer',
               sexp.Symbol('desc:'),
               u"Kyle's computer",
               sexp.Symbol('messages:'),
               [[sexp.Symbol('message'),
                 sexp.Symbol('name:'),
                 'say',
                 sexp.Symbol('desc:'),
                 'Says a phrase',
                 sexp.Symbol('arguments:'),
                 [[sexp.Symbol('argument'),
                   sexp.Symbol('name:'),
                   'tex"t',
                   sexp.Symbol('type:'),
                   sexp.Symbol('string')]]]]]]]

def timer(NUM=100):
    def _timer(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            gc.disable()
            start = time.time()
            for i in range(NUM):
                func(*args, **kwargs)
            diff = time.time() - start
            print "Tested %s throughput: %0.2f trials / sec" % (func.__name__, NUM / diff)
        return _wrapper
    return _timer

@timer(NUM=1000)
def runner():
    sexp.write(sexp_data)


if __name__ == '__main__':
    import timeit
    runner()
    #import doctest
    #doctest.testmod()
