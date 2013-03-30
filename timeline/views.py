# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader

#from polls.models import Poll

# Create your views here.
def index(request):
    template = loader.get_template('oc/timeline.html')
    context = Context({})
    return HttpResponse(template.render(context))
