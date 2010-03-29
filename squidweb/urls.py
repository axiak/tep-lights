from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     url(r'^/?$', 'squidweb.squid.views.servers', name='servers'),
     (r'^media/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT}),
     url(r'^(?P<server>\w+)/?$', 'squidweb.squid.views.devices', name='devices'),
     url(r'^(?P<server>\w+)/(?P<device>[^/]+)/(?P<message>[^/]+)/?$', 'squidweb.squid.views.messageform', name='messageform'),

    # Example:
    # (r'^squidweb/', include('squidweb.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
