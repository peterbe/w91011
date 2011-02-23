from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.start_page, name='start-page'),
    url(r'^login/$', views.start_page, name='login'),
    url(r'^welcome/$', views.welcome, name='welcome'),
)