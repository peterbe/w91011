# python
import datetime
import logging

# django
from django.conf import settings
from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
from django.db import transaction

class UserProfile(models.Model):
    """Some extra fields to descibe a user"""
    user = models.ForeignKey(User)

    class Meta:
        ordering = ('user__username',)

    def __unicode__(self):
        return u'%s' % self.user
