from django.conf import settings
from django.contrib import admin

from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

class FlatPageAdmin(FlatPageAdminOld):
    class Media:
        js = (settings.TINYMCE_JS_URL,
              '/static/js/textareas.js',
              )

# We have to unregister it, and then reregister
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
