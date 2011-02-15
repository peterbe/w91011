import datetime
from django.db import models
from django.contrib.auth.models import User

class StringArrayField(models.CharField):
    __metaclass__ = models.SubfieldBase
    description = "basic field for storing string arrays"
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 500)
        super(StringArrayField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if not value:
            return list()
        return value.split('|')

    def get_prep_value(self, value):
        return '|'.join(value)

class Food(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class RSVP(models.Model):
    user = models.ForeignKey(User, unique=True)
    coming = models.BooleanField(default=True,
      choices=[(True, "Yes!"), (False, "Unfortunately not")])
    people = models.StringArrayField()
    no_people = models.IntegerField(default=1)
    food = models.ManyToManyField(Food)
    other_dietary_requirements = models.TextField(blank=True)

    add_date = models.DateTimeField(default=datetime.datetime.now)
    modify_date = models.DateTimeField(default=datetime.datetime.now)
