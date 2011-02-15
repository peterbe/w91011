from optparse import make_option

from django.core.management.base import NoArgsCommand, BaseCommand
from django.contrib.auth.models import User

UNSAFE_PASSWORD = "test123"

class Command(NoArgsCommand):
    help = 'List users that have an unsafe password'
    option_list = BaseCommand.option_list + (
        make_option('--disable',
        action='store_true',
        dest='disable',
        default=False,
        help='Disable users with unsafe passwords.'),
    )


    def handle_noargs(self, **options):
        all_users = User.objects.all()
        unsafe_users = []
        for user in all_users:
            if user.check_password(UNSAFE_PASSWORD):
                unsafe_users.append(user)
        print "found %d unsafe users" % len(unsafe_users)
        disabled_users = 0
        for user in unsafe_users:
            print "%s" % user.email
            if options["disable"]:
                if user.is_active:
                    user.is_active = False
                    user.save()
                    disabled_users += 1
        if options["disable"]:
            print "%d users disabled" % disabled_users

