from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

class InvitationKeysMiddleware(object):
    def process_request(self, request):
        invitation_key = request.GET.get('invitation', request.GET.get('i'))
        if invitation_key:
            invitation_key = invitation_key.strip()
            if invitation_key not in settings.INVITATION_KEYS:
                invitation_key = invitation_key.decode('rot13')
            if invitation_key in settings.INVITATION_KEYS:
                request.session['invited'] = True
                return HttpResponseRedirect(reverse('website:welcome'))
            else:
                return HttpResponse("Invalid invitation link. Sorry.")