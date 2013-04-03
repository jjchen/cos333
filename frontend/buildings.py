import requests
from frontend.models import Building
from frontend.models import BuildingAlias


resp = requests.get("http://etcweb.princeton.edu/MobileFeed/map/json.php")
json_obj = resp.json()

buildings = json_obj['location']

for building in buildings:
	latitude = building['latitude']
	longitude = building['longitude']

	newBuilding = Building(name=building['name'], lat=latitude, lon=longitude)
	newBuilding.save()

	newBuildingAlias = BuildingAlias(alias = building['name'], building = newBuilding)
	newBuildingAlias.save()

	for alias in building['aliases']:
		newBuildingAlias = BuildingAlias(alias=alias, building=newBuilding)
		newBuildingAlias.save()