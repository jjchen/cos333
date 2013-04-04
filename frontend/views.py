from django.shortcuts import render
from frontend.models import NewEvent
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
	# get fields
	new_name = request.POST['event_name']
	new_date = request.POST['date']
	new_time = request.POST['start_time']
	new_location = request.POST['location']

	# search for lat lon of location
	latitude = None
	longitude = None
	buildingAlias = BuildingAlias.objects.filter(alias=new_location)
	if (buildingAlias):
		building = buildingAlias[0].building
		latitude = building.lat
		longitude = building.lon
	

	# format date
	date = datetime.datetime.strptime(new_date, "%Y-%m-%d").date()

	# format time
	time = datetime.datetime.strptime(new_time, "%H:%M").time()

	# add to database
	new_event = NewEvent(name=new_name, date=date, time=time, location=new_location, lat=latitude, lon=longitude)
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

