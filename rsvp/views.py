from random import shuffle
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages#
from django.contrib.auth.decorators import login_required

from forms import RSVPForm
from models import RSVP, Food
from utils import render

@render('rsvp/start.html')
@login_required
@transaction.commit_on_success
def start(request):
    if request.method == "POST":
        form = RSVPForm(data=request.POST)
        if form.is_valid():
            rsvp, __ = RSVP.objects.get_or_create(user=request.user)
            people = form.cleaned_data['people']
            people = [x.strip() for x in people.splitlines() if x.strip()]
            rsvp.people = people
            rsvp.no_people = len(people)
            rsvp.song_requests = form.cleaned_data['song_requests']
            rsvp.save()
            return HttpResponseRedirect(reverse('rsvp:food'))
    else:
        initial = dict(people=request.user.first_name)
        form = RSVPForm(initial=initial)
    return locals()

@render('rsvp/food.html')
@login_required
def food(request):
    rsvp = RSVP.objects.get(user=request.user)
    i = 0
    mapping = {}
    for name in rsvp.people:
        mapping[name] = None
    for x in rsvp.food.all():
        print rsvp.people[i]
        print x.id, x.title
        i += 1
    names = mapping.items()
    foods = Food.objects.all()
    if request.method == "POST":
        raise NotImplementedError

    return locals()
