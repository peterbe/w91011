from random import shuffle
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages#
from django.contrib.auth.decorators import login_required

from forms import RSVPForm, FoodExtraForm
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
            if not request.POST.get('coming'):
                rsvp.coming = False
                rsvp.save()
                return HttpResponseRedirect(reverse('rsvp:shame'))
            people = form.cleaned_data['people']
            people = [x.strip() for x in people.splitlines() if x.strip()]
            rsvp.people = people
            rsvp.no_people = len(people)
            rsvp.song_requests = form.cleaned_data['song_requests']
            rsvp.save()
            return HttpResponseRedirect(reverse('rsvp:food'))
    else:
        if RSVP.objects.filter(user=request.user):
            rsvp = RSVP.objects.get(user=request.user)
            people = rsvp.people
            if request.user.first_name not in people:
                people.insert(0, request.user.first_name)
            initial = dict(coming=rsvp.coming,
                           people='\n'.join(people),
                           song_requests=rsvp.song_requests)
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
        extra_form = FoodExtraForm(data=request.POST)
        if extra_form.is_valid():
            rsvp.other_dietary_requirements = \
              extra_form.cleaned_data['other_dietary_requirements']
            rsvp.save()

        i = 1
        for name, __ in names:
            print repr(name), i
            key = 'food_%s' % i
            pk = request.POST[key]
            print "PK", repr(pk)
            print [(x.pk, repr(x)) for x in Food.objects.all()]
            food = Food.objects.get(pk=pk)
            rsvp.food.add(food)
            i += 1
        rsvp.save()

        return HttpResponseRedirect(reverse('rsvp:thanks'))

    else:
        extra_form = FoodExtraForm(initial=\
          dict(other_dietary_requirements=rsvp.other_dietary_requirements))

    return locals()

@render('rsvp/shame.html')
@login_required
def shame(request):
    return locals()

@render('rsvp/thanks.html')
@login_required
def thanks(request):
    return locals()
