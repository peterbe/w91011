from random import shuffle
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.flatpages.models import FlatPage
from utils import render
from forms import SignupForm, LoginForm
from django.contrib.auth import load_backend, login
from rsvp.models import RSVP, Food

WELCOME_MESSAGE = """
Hi %(first_name)s,

Thank you for logging in to our wedding site.
Since it's an invitation-only site you have to have an account.
If you ever need to log in again, do so with your email address
(%(email)s) and the password is: %(password)s

--
Puss och kram, Peter & Ashley
"""

@render('website/start_page.html')
def start_page(request):
    if request.user.is_authenticated():
        try:
            rsvp = RSVP.objects.get(user=request.user)
        except RSVP.DoesNotExist:
            rsvp = None
        flat_pages = FlatPage.objects.all()
    else:
        if request.method == "POST":
            form = LoginForm(data=request.POST)
            if form.is_valid():
                return HttpResponseRedirect('/?logged_in=HELLYEAH')
        else:
            form = LoginForm()
    return locals()

@render('website/welcome.html')
@transaction.commit_on_success
def welcome(request):
    if not request.session.get('invited'):
        return HttpResponse("Not invited.")
    if request.user.is_authenticated():
        # the welcome page is not for logged in people
        return HttpResponseRedirect(reverse('website:start-page'))

    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = '%s_%s' % (first_name, last_name)
            username = username.lower()
            email = form.cleaned_data['email']
            #password = form.cleaned_data['password']
            user = User.objects.create(
              username=username,
              first_name=first_name,
              last_name=last_name,
              email=email,
            )
            password = list('password123')
            shuffle(password)
            password = ''.join(password)
            user.set_password(password)
            user.save()

            for backend in settings.AUTHENTICATION_BACKENDS:
                if user == load_backend(backend).get_user(user.pk):
                    user.backend = backend

            if hasattr(user, 'backend'):
                login(request, user)

            send_mail("Welcome to %s" % settings.PROJECT_NAME,
                      WELCOME_MESSAGE % dict(first_name=user.first_name,
                                             email=user.email,
                                             password=password),
                      settings.WEBMASTER_EMAIL,
                      [user.email])

            return HttpResponseRedirect(reverse('rsvp:start'))

    else:
        form = SignupForm()
    return locals()
