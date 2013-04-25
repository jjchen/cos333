from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

import requests
from frontend.models import NewEvent
import datetime
import time

@dajaxice_register
def sayhello(request):
    #return simplejson.dumps({'message':'Hello World'})
    resp = requests.get("http://etcweb.princeton.edu/MobileFeed/events/?fmt=json")
    json_obj = resp.json()
	events = json_obj['events']

	for event in events:
	   name = event['title']
	   building = event['locationName']
	   latitude = event['latitude']
	   longitude = event['longitude']
	   startDate = event['startDate']
	   startTime = event['startTime']

		# format date
		date = datetime.datetime.strptime(startDate['0'], "%Y-%m-%d").date()

		parts = startTime.split()

		# format time
		time = datetime.datetime.strptime(parts[0], "%H:%M:%S %z").time()

		# make into tags
		categories = event['categories']

		new_event = NewEvent(name=name, date=date, time=time, location=building, lat=latitude, lon=longitude)
		new_event.save()
