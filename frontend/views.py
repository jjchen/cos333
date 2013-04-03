from django.shortcuts import render
from frontend.models import NewEvent
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
import datetime

# Create your views here.
def index(request):
	events_list = NewEvent.objects.all()
	context = {'events_list': events_list, 'user': request.user, 'map_event_name': "Some Event", 'map_event_location': "Frist Campus Center"}
	return render(request, 'frontend/map.html', context)

def add(request):
	# get fields
	new_name = request.POST['event_name']
	new_date = request.POST['date']
	new_time = request.POST['start_time']
	new_location = request.POST['location']

	# search for lat lon of location
	buildingAlias = BuildingAlias.objects.filter(alias=new_location)
	if (buildingAlias):
		building = buildingAlias.building
		latitude = building.lat
		longitude = building.lon
	
	# add to database
	new_event = NewEvent(name=new_name, date=datetime.date.today(), time=datetime.time(5,0,0,0), location=new_location, lat=latitude, lon=longitude)
	new_event.save()

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

