# python
import datetime
from urlparse import urlparse, urlunparse
from hashlib import md5

# django
from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import logout as django_logout
from django.core.mail import send_mail
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.cache import cache
from django.template import Context, loader
from django.contrib.auth import load_backend, login

# app
from models import UserProfile
from utils import render, staff_required, nicepass, email_to_username, \
  niceboolean, superuser_required
from forms import *


def get_user_profile(user):
    try:
        return user.get_profile()
    except UserProfile.DoesNotExist:
        return UserProfile.objects.create(user=user)

def redirecting(request):
    """page that redirects to the homepage by javascript so you get a nice
    user-friendly message saying it's redirecting you.
    """
    redirect_to = request.GET.get('next','/')
    # paranoia
    if redirect_to.split('?')[0] == reverse('users:redirecting'):
        redirect_to = '/'
    elif settings.LOGIN_URL in redirect_to:
        # this shouldn't happen!
        if request.user.is_authenticated():
            redirect_to = '/'

    if '?next=' in redirect_to:
        redirect_to = redirect_to.split('?next=')[0]

    redirect_to_absolute_url = request.build_absolute_uri()
    redirect_to_absolute_url = list(urlparse(redirect_to_absolute_url))
    redirect_to_absolute_url[2] = redirect_to
    if '?' in redirect_to:
        redirect_to_absolute_url[4] = ''
    elif redirect_to_absolute_url[4].startswith('next='):
        redirect_to_absolute_url[4] = ''

    redirect_to_absolute_url = urlunparse(redirect_to_absolute_url)

    return render_to_response('users/redirecting.html', {
        'redirect_to': redirect_to,
        'redirect_to_absolute_url': redirect_to_absolute_url,
        'page_title': "Redirecting...",
    }, context_instance=RequestContext(request))

def logout(request, *args, **kwargs):
    return django_logout(request, next_page='/',
                         *args, **kwargs)
