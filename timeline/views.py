# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
#from polls.models import Poll

# Create your views here.
def index(request):
#    template = loader.get_template('timeline/map.html')
#    context = Context({})
 #   return HttpResponse(template.render(context))
    return render_to_response('timeline/timeline.html')
    return render_to_response('timeline/fancytimeline.html')