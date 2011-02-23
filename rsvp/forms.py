from django import forms
from django.forms.widgets import HiddenInput
from utils.forms import BaseForm
from models import RSVP, Food

class RSVPForm(BaseForm):
    people = forms.CharField(required=True, help_text="Write one name per line",
      widget=forms.widgets.Textarea(attrs=dict(cols=30, rows=2)))
    #food = forms.ModelChoiceField(queryset=Food.objects)
    #other_dietary_requirements = forms.CharField(required=False,
    #  help_text="Anything extra we should know like nut allergy",
    #  widget=forms.widgets.Textarea(attrs=dict(cols=30, rows=2)))
    song_requests = forms.CharField(label="Song request", required=False,
      widget=forms.widgets.Textarea(attrs=dict(cols=30, rows=2)))
    def __init__(self, *args, **kwargs):
        super(RSVPForm, self).__init__(*args, **kwargs)
        #self.fields['user'].widget = HiddenInput()

class FoodExtraForm(BaseForm):
    other_dietary_requirements = forms.CharField(required=False,
      help_text="Anything extra we should know like nut allergy",
      widget=forms.widgets.Textarea(attrs=dict(cols=30, rows=2)))
