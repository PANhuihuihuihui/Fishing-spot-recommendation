import googlemaps
import json

API_KEY = "Your API Key goe"
gmaps = googlemaps.Client(key=API_KEY)

def get_location(name):
    geocode_result = gmaps.geocode(name)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None, None

def add_location_to_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    for county, lakes in data.items():
        for lake_name in lakes:
            lat, lng = get_location(f"{lake_name}, {county} county ,MI")
            data[county][lake_name]["latitude"] = lat
            data[county][lake_name]["longitude"] = lng

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)

add_location_to_json('lake_data.json')
