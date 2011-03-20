from django.contrib import admin

from models import RSVP, Food
class FoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)

class RSVPAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'coming',)

admin.site.register(Food, FoodAdmin)
admin.site.register(RSVP, RSVPAdmin)
