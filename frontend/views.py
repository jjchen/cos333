from django.shortcuts import render
from frontend.models import NewEvent

# Create your views here.
def index(request):
	events_list = NewEvent.objects.all()
	context = {'events_list': events_list}
	return render(request, 'frontend/map.html', context)
