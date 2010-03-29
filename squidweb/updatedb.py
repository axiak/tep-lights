#!/usr/bin/env python
import sys
import os
import datetime
import time
from django.core.management import setup_environ

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from squidweb import settings
setup_environ(settings)

from squidnet import squidclient as sc
from squidweb.squid.models import ServerInfo

import pydaemon

def main():
    # our main event loop is inside SquidInfo
    pydaemon.createDaemon()
    info = sc.SquidInfo(callback=handle_info)
    info.start()
    while True:
        time.sleep(60)


def handle_info(info, servers):
    # Handle all of the nice servers...
    for key, value in servers.items():
        s = ServerInfo.from_info(value)
        s.save()

    # Now handle all of the random ones
    in_danger = ServerInfo.objects.filter(expires__lte = datetime.datetime.now() +
                                          datetime.timedelta(seconds = 20))
    for server in in_danger:
        info.ping(server.info.host)
        
    # Now delete all of the old ones
    ServerInfo.objects.filter(expires__lte = datetime.datetime.now() -
                              datetime.timedelta(seconds=7200)).delete()

if __name__ == '__main__':
    main()
