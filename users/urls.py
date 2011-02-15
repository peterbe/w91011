from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
        url(r'^logout/$', views.logout, name='logout'),
        url(r'^admin/$', views.admin_home, name='admin'),
        url(r'^admin/add-user/$', views.add_user, name='add-user'),
        url(r'^admin/user/(?P<username>[\w\-]+)/edit/$', views.edit_user, name='edit-user'),
        url(r'^admin/user/(?P<username>[\w\-]+)/edit/password/$', views.edit_user_password, name='edit-user-password'),
        url(r'^admin/user/(?P<username>[\w\-]+)/setup-default-assessments/$', views.setup_default_assessments, name='setup-default-assessments'),
        #url(r'^register/$', views.register, name='register'),
        #url(r'^insufficient-privileges/$', views.insufficient_privileges, name='insufficient-privileges'),
        url(r'^redirecting/$', views.redirecting, name='redirecting'),
        url(r'^settings/$', views.user_settings, name='user-settings'),
        url(r'^settings/password/$', views.change_password, name='change-password'),
        #url(r'^debug-logins/$', views.debug_logins, name='debug_logins'),
        url(r'^reset-password/$', views.reset_password, name='reset-password'),
        url(r'^reset-password/done/$', views.reset_password_done, name='reset-password-done'),
        url(r'^rp/(\d+)/([a-f0-9]+)/([a-f0-9]{32})/$', views.reset_password_recover, name='reset-password-recover'),
)
