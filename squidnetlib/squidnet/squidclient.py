#!/usr/bin/env python
import socket
import sys
import traceback
import shlex
from threading import Thread

from squidnet import sexp, squidprotocol as s

class SquidInfo(Thread) :
    def __init__(self, callback=None) :
        Thread.__init__(self)
        self.servers = {}
        self.setDaemon(True)
        self.callback = callback

    def run(self) :
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(10)
        self.new_servers = {}
        while True:
            try :
                self.sock.sendto("info", ('<broadcast>', s.SQUIDNET_BROADCAST_PORT))
                while True :
                    if self.callback:
                        self.callback(self, self.servers)
                    self.servers = self.new_servers
                    self.new_servers = {}
                    (message, address) = self.sock.recvfrom(4096)
                    if len(message) :
                        try :
                            xs = sexp.read_all(message)
                            for x in xs :
                                serv = s.SquidServer.load_sexp(x)
                                # hopefully server names are unique
                                self.new_servers[serv.name] = serv
                        except socket.error :
                            pass #timeout
                        except :
                            print "bad server response. ignoring: "+message
                            traceback.print_exc()
            except socket.error :
                pass # timeout
            except :
                traceback.print_exc()
        self.sock.close()
    def ping(self, dest_addr) :
        self.sock.sendto("info", (dest_addr, s.SQUIDNET_BROADCAST_PORT))

    def request(self, server, device, message, args={}) :
        if server in self.servers :
            r = self.servers[server].request(device, message, args)
            dest = (self.servers[server].host, self.servers[server].port)
            self.sock.sendto(sexp.write(r), dest)
            print "sent "+sexp.write(r)
        else :
            raise Exception("No such server to request: "+server)

if __name__=="__main__" :
    print "SquidNet client shell"
    info = SquidInfo()
    info.start()
    while True :
        try:
            i = raw_input("> ")
            l = shlex.split(i)
            if l[0] == "ping" :
                print "Pinging",l[1]
                info.ping(l[1])
                #info.ping(l[1])
            elif l[0] == "servers" :
                for serv in info.servers.keys() :
                    print serv
            elif l[0] == "devices" :
                for d in info.servers[l[1]].devices :
                    print "%s\t%s" % (d.name, d.desc)
            elif l[0] == "messages" :
                for m in info.servers[l[1]].get_device(l[2]).messages :
                    #print sexp.write(m.get_sexp())
                    print m.name,
                    for a in m.arguments :
                        print "("+a.name,str(a.argtype)+")",
                    print "- %s" % (m.desc)
            elif l[0] == "request" :
                c = i.split(" ", 4)
                if len(c) < 5 :
                    c.append("")
                m = info.servers[c[1]].get_device(c[2]).get_message(c[3])
                args = m.decode_sexp_args(sexp.read_all(c[4]))
                info.request(c[1], c[2], c[3], args)
            elif l[0] == "dump" :
                print sexp.write(info.servers[l[1]].get_sexp())
            elif l[0] in ('quit', 'exit'):
                break
        except (KeyboardInterrupt, EOFError) :
            break
        except :
            traceback.print_exc()
            pass
