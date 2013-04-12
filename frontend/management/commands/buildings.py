import requests
from frontend.models import Building
from frontend.models import BuildingAlias
from django.core.management.base import BaseCommand, CommandError
import json
import urllib2

class Command(BaseCommand):

	def handle(self, *args, **options): 

		#resp = requests.get("http://etcweb.princeton.edu/MobileFeed/map/json.php")
		resp = urllib2.urlopen('http://etcweb.princeton.edu/MobileFeed/map/json.php')
		json_obj = json.load(resp)
		#json_obj = resp.json()

		buildings = json_obj['location']

		for building in buildings:

			try:
				Building.objects.get(name = building['name'])
			except Building.DoesNotExist:
				latitude = building['latitude']
				longitude = building['longitude']

				newBuilding = Building(name=building['name'], lat=latitude, lon=longitude)
				newBuilding.save()

				newBuildingAlias = BuildingAlias(alias = building['name'], building = newBuilding)
				newBuildingAlias.save()

				for alias in building['aliases']:
					newBuildingAlias = BuildingAlias(alias=alias, building=newBuilding)
					newBuildingAlias.save()