# Create your views here.

from utils import render

@render('website/start_page.html')
def start_page(request):
    return locals()
