from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.start, name='start'),
    url(r'^food/$', views.food, name='food'),
    url(r'^shame/$', views.shame, name='shame'),
    url(r'^thanks/$', views.thanks, name='thanks'),
)