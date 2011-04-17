from django.contrib import admin

from models import RSVP, Food
class FoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','rsvped')

    def rsvped(self, obj):
        count = 0
        for rsvp in RSVP.objects.all():
            for value in rsvp.food.values():
                if int(value) == obj.pk:
                    count += 1
        return count
    rsvped.short_description = "RSVP'ed"

class RSVPAdmin(admin.ModelAdmin):
    list_display = ('people_list', 'coming','food_brief', 'other')

    def people_list(self, obj):
        if obj.people:
            return '#%s ' % obj.no_people + ', '.join(obj.people)
        else:
            return '(%s)' % obj.user
    people_list.short_description = "People"

    def food_brief(self, obj):
        if not obj.people:
            return ''
        lines = []
        for name, pk in obj.food.items():
            name = name.split()[0]
            food = Food.objects.get(pk=pk)
            lines.append('%s: %s' % (name, food.title))
        lines.sort()
        return '; '.join(lines)
    food_brief.short_description = "Food"

    def other(self, obj):
        bits = []
        if obj.other_dietary_requirements:
            bits.append("Other dietary requirements: %s" % \
              obj.other_dietary_requirements)
        if obj.song_requests:
            bits.append('Song requests: %s' % \
              obj.song_requests)
        return '; '.join(bits)
    other.short_description = "Other bits"


admin.site.register(Food, FoodAdmin)
admin.site.register(RSVP, RSVPAdmin)
