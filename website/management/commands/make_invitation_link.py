from random import shuffle
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "New link for inviations"

    def handle(self, **options):
        keys = list(settings.INVITATION_KEYS)
        shuffle(keys)
        print "/?i=%s" % keys[0].encode('rot13')
