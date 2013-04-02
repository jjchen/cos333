import requests

resp = requests.get("http://etcweb.princeton.edu/MobileFeed/map/json.php")
json_obj = resp.json()

buildings = json_obj['location']

for building in buildings:
	latitude = building['latitude']
	longitude = building['longitude']

	newBuilding = Building(name=building['name'], lat=latitude, long=longitude)
	newBuilding.save()

	for alias in building['aliases']:
		newBuilding = Building(name=alias, lat=latitude, long=longitude)
		newBuilding.save()