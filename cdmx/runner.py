#!/usr/bin/python
import sys
import os
import time
import signal

PROG = os.path.join(os.path.dirname(__file__), 'src', 'jackserver')

def main():
    main_prog, plugins = parse_args()
    pids = []
    pids.append(os.spawnv(os.P_NOWAIT, main_prog[0], main_prog))
    time.sleep(0.05)
    for plugin in plugins:
        pids.append(os.spawnv(os.P_NOWAIT, plugin[0], plugin))
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt, e:
        for pid in pids:
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass


def parse_args():
    args = sys.argv
    prog = []
    plugins = []
    plugin = False
    for i, arg in enumerate(sys.argv[1:]):
        if arg == '--plugin':
            plugin = True
            plugins.append([])
            continue
        if not plugin:
            prog.append(arg)
        else:
            plugins[-1].append(arg)
    if not prog:
        prog.append(PROG)
    return prog, plugins

if __name__ == '__main__':
    main()
