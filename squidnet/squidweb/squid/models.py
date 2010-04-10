import datetime
import binascii

from django.db import models

from squidnet import squidprotocol
from squidnet import sexp


__all__ = ('ServerInfo',)

class ServerInfo(models.Model):
    lastupdate = models.DateTimeField()
    server_name = models.CharField(max_length=255, primary_key=True)
    pickled_data = models.TextField(editable=False)
    ttl = models.IntegerField(default=120)
    expires = models.DateTimeField(db_index=True)

    def __unicode__(self):
        return u'<ServerInfo: %s; %s>' % (self.server_name, self.lastupdate)
    __repr__ = __unicode__


    def _get_info(self):
        if not hasattr(self, '_info'):
            try:
                self._info = squidprotocol.SquidServer.load_sexp(sexp.read_all(str(self.pickled_data))[0])
            except int:
                raise ValueError("No data set yet")
        return self._info

    def _set_info(self, info):
        self.pickled_data = sexp.write(info.get_sexp())
        self._info = info

    info = property(_get_info, _set_info)

    def save(self, *args, **kwargs):
        self.ttl = self.ttl or 120
        self.lastupdate = self.lastupdate or datetime.datetime.now()
        self.expires = self.lastupdate + datetime.timedelta(seconds = self.ttl)
        return super(ServerInfo, self).save(*args, **kwargs)

    @property
    def devices(self):
        return self.info.devices

    @classmethod
    def from_info(cls, serverinfo):
        serverobj = cls()
        serverobj.info = serverinfo
        serverobj.server_name = serverinfo.name
        serverobj.lastupdate = datetime.datetime.now()
        return serverobj

    @models.permalink
    def get_absolute_url(self):
        return ('devices', (), {'server': self.server_name})
