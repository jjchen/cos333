import datetime
import time
import requests

from frontend.models import NewEvent
from social_auth.models import UserSocialAuth
from facepy import GraphAPI

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

    request_user = '290031427770649'
    instance = UserSocialAuth.objects.get(user=request_user, provider='facebook')
    token = instance.tokens
    graph = GraphAPI(token)

    event_path = "https://graph.facebook.com/290031427770649/events"
    event_data = {
        'name' : "Test Event",
        'start_time' : "2013-07-04",
        'location' : "someplace",
        'privacy_type' : "SECRET"
        }

    result = graph.post(event_path, event_data)

    if result.get('id', False):
        "Successfully Created Event"
    else:
        "Failure"
