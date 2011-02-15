# python

# django
from django.contrib import admin
from django.conf.urls.defaults import *

# app
from models import UserProfile



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ()
    #list_filter = ()


admin.site.register(UserProfile, UserProfileAdmin)
