from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^rsvp/', include('rsvp.urls',
                        namespace='rsvp',
                        app_name='rsvp')),
    (r'^users/', include('users.urls',
                                  namespace='users',
                                  app_name='users')),
    (r'', include('website.urls',
                                  namespace='website',
                                  app_name='website')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^admin/', include(admin.site.urls)),
)

import django.views.static
urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', django.views.static.serve,
      {'document_root': settings.MEDIA_ROOT,
       'show_indexes': settings.DEBUG}),
    (r'^images/(?P<path>.*)$', django.views.static.serve,
     {'document_root': settings.MEDIA_ROOT + '/images',
       'show_indexes': settings.DEBUG}),
    (r'^css/(?P<path>.*)$', django.views.static.serve,
      {'document_root': settings.MEDIA_ROOT + '/css',
       'show_indexes': settings.DEBUG}),
    (r'^js/tiny_mce/(?P<path>.*)$', django.views.static.serve,
      {'document_root': '/home/peterbe/virtualenvs/w91011/lib/python2.6/site-packages/pages/media/js/tiny_mce',
       'show_indexes': settings.DEBUG}),
    (r'^js/(?P<path>.*)$', django.views.static.serve,
      {'document_root': settings.MEDIA_ROOT + '/js',
       'show_indexes': settings.DEBUG}),
)
