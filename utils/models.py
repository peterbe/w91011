from django.db import models

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

class TextArrayField(models.TextField):

    __metaclass__ = models.SubfieldBase

    description = "basic field for storing large string arrays"

    def __init__(self, *args, **kwargs):
        super(TextArrayField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if not value:
            return list()
        return value.split('|||')

    def get_prep_value(self, value):
        return '|||'.join(value)
    