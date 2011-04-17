from django import forms
from django.forms.widgets import HiddenInput
from utils.forms import BaseForm
from models import RSVP, Food

class RSVPForm(BaseForm):
    people = forms.CharField(
      label="People coming (including your name write one name per line)",
      required=True, help_text="",
      widget=forms.widgets.Textarea(attrs=dict(cols=30, rows=2)))
    #food = forms.ModelChoiceField(queryset=Food.objects)
    #other_dietary_requirements = forms.CharField(required=False,
    #  help_text="Anything extra we should know like nut allergy",
    #  widget=forms.widgets.Textarea(attrs=dict(cols=30, rows=2)))
    def __init__(self, *args, **kwargs):
        super(RSVPForm, self).__init__(*args, **kwargs)
        #self.fields['user'].widget = HiddenInput()

class FoodExtraForm(BaseForm):
    other_dietary_requirements = forms.CharField(required=False,
      label="Other dietary requirements (anything extra we should know like nut allergy)",
      widget=forms.widgets.Textarea(attrs=dict(cols=30, rows=2)))


class SongRequestsForm(BaseForm):
    song_requests = forms.CharField(
      label="Reception song requests (enter one song per line)",
      required=False,
      widget=forms.widgets.Textarea(attrs=dict(cols=30, rows=2)),
      )
