from django.conf import settings

def context(request):
    context = {}
    context['DEBUG'] = settings.DEBUG
    context['PROJECT_NAME'] = settings.PROJECT_NAME
    return context
