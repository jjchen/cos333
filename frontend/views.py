from django.shortcuts import render
from frontend.models import NewEvent
import datetime

# Create your views here.
def index(request):
	events_list = NewEvent.objects.all()
	context = {'events_list': events_list}
	return render(request, 'frontend/map.html', context)

def add(request):
	# get fields
	new_name = request.POST['event_name']
	new_date = request.POST['date']
	new_time = request.POST['start_time']
	new_location = request.POST['location']
	
	# add to database
	new_event = NewEvent(name=new_name, date=datetime.date.today(), time=datetime.time(5,0,0,0), location=new_location)
	new_event.save()

	# return to index
	return HttpResponseRedirect(reverse('frontend:index'))