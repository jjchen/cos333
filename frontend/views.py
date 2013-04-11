from django.shortcuts import render
from frontend.models import NewEvent
from frontend.models import NewEventForm
from frontend.models import BuildingAlias
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
import datetime

# Create your views here.
def index(request):
	if request.method =='POST':
		query = request.POST['search_query']
		events_list = NewEvent.objects.filter(Q(name__icontains=query) | Q(location__icontains=query)).order_by("date", "time")
		show_list = True
	else:
		events_list = NewEvent.objects.all().order_by("date", "time")
		show_list = False

	context = {'events_list': events_list, 'user': request.user, 'show_list': show_list}
	return render(request, 'frontend/map.html', context)

def add(request):
	# django'd the forms
	f = NewEventForm(request.POST)
	# prints errors for now - form will currently not validate if you send it as empty
	# will soon print error messages
	# print f.errors
	new_event = f.save(commit=False)

	#new_name = request.POST['event_name']
	#new_date = request.POST['date']
	#new_time = request.POST['start_time']
	#new_location = request.POST['location']

	# search for lat lon of location
	latitude = None
	longitude = None
	buildingAlias = BuildingAlias.objects.filter(alias=new_event.location)
	if (buildingAlias):
		building = buildingAlias[0].building
		latitude = building.lat
		longitude = building.lon
	
	# add to database
	# new_event.date = datetime.date.today()
	#new_event.start_time = datetime.time(5,0,0,0)
	new_event.lat = latitude
	new_event.lon = longitude
	#new_event = NewEvent(name=new_name, date=datetime.date.today(), time=datetime.time(5,0,0,0), location=new_location, lat=latitude, lon=longitude)
	new_event.save()
	f.save_m2m()

	# return to index
	return HttpResponseRedirect(reverse('frontend:index'))
	#return HttpResponse("HI")

def search(request):
	query = request.POST['search_query']

	results = NewEvent.objects.filter(Q(name__icontains=query) | Q(location__icontains=query))

	html = "<html><body>Search Results: %s" % query
	for event in results:
		html += "<br/> %s <br/>" % event.name
	html += "</body></html>"

	return HttpResponse(html)

