import datetime
import socket
import threading
import itertools

from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.views.generic import simple
from django.core.urlresolvers import reverse

from squidweb.squid import forms as squidforms
from squidweb.squid.models import *

from squidnet import sexp


ajax_success = HttpResponse('{"Result":"Success"}', mimetype='application/json')
ajax_fail = HttpResponse('{"Result":"Fail"}', mimetype='application/json')

def servers(request):
    servers = ServerInfo.objects.filter(expires__gte = datetime.datetime.now())
    return simple.direct_to_template(request, 'squid/servers.html',
                                     {'servers': servers})


def devices(request, server=None):
    success = request.GET.get('success', False)
    if server:
        serverinfo = get_object_or_404(ServerInfo,
                                       pk = server,
                                       expires__gte = datetime.datetime.now())
        devices = serverinfo.devices
        for device in devices:
            device.server = serverinfo
    else:
        serverinfo = None
        devices = []
        for server in ServerInfo.objects.filter(expires__gte = datetime.datetime.now()):
            for device in server.devices:
                devices.append(device)
                device.server = server

    return simple.direct_to_template(request, 'squid/serverdetail.html',
                                     {'server': serverinfo,
                                      'success': success,
                                      'devices': devices})



def messageform(request, server, device, message):
    serverinfo = get_object_or_404(ServerInfo,
                                   pk = server,
                                   expires__gte = datetime.datetime.now())
    for deviceobj in serverinfo.devices:
        if deviceobj.name == device:
            break
    else:
        raise Http404

    for messageobj in deviceobj.messages:
        if messageobj.name == message:
            break
    else:
        raise Http404

    if not messageobj.arguments:
        send_request(serverinfo, device, message, {})
        return redirect('%s?success=1' % reverse('all-devices'))

    FormClass = squidforms.message_form_factory(messageobj)

    if request.method == "POST":
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            send_request(serverinfo, device, message, form.create_squid_args())
            if request.is_ajax():
                return ajax_success
            return redirect('%s?success=1' % reverse('all-devices'))
    else:
        form = FormClass()

    if request.is_ajax():
        return ajax_fail

    return simple.direct_to_template(request, 'squid/messageform.html',
                                     {'form': form,
                                      'server': serverinfo})


class SockData(threading.local):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(10)

sockdata = SockData()

def send_request(serverinfo, device, message, args):
    r = serverinfo.info.request(device, message, args)
    dest = serverinfo.info.host, serverinfo.info.port
    sockdata.sock.sendto(sexp.write(r), dest)
