from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.start_page, name='start-page'),
)