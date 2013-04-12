import requests
from frontend.models import NewEvent
from django.core.management.base import BaseCommand, CommandError
import datetime
import time
import json
import urllib2

class Command(BaseCommand):

	def handle(self, *args, **options): 

		feeds = ["http://etcweb.princeton.edu/MobileFeed/events/?fmt=json", "http://etcweb.princeton.edu/webfeeds/events/roxen/?fmt=json", "http://etcweb.princeton.edu/webfeeds/events/usg/?fmt=json"]
		for url in feeds:
			resp = urllib2.urlopen(url)
			json_obj = json.load(resp)

			events = json_obj['events']

			for event in events:
				try:
					NewEvent.objects.get(name = event['title'])
				except NewEvent.DoesNotExist:
					name = event['title']
					building = event['locationName']
					latitude = event['latitude']
					longitude = event['longitude']
					startDate = event['startDate']
					startTime = event['startTime']
					endDate = event['endDate']
					endTime = event['endTime']
					description = event['description']
					#audience = event['audience']
					#tags = event['categories']['categoryName']

					# format date
					date = datetime.datetime.strptime(startDate['0'], "%Y-%m-%d").date()

					parts = startTime.split()

					# format time
					time = datetime.datetime.strptime(parts[0], "%H:%M:%S").time()

					# make into tags
					categories = event['categories']

					new_event = NewEvent(name=name, date=date, time=time, location=building, lat=latitude, lon=longitude, tags="hi")
					new_event.save()
