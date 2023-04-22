import json

def convert_json_format(json_data):
    # Find unique set of all species
    all_species = set()
    for county_data in json_data.values():
        for spot_data in county_data.values():
            if spot_data["fish_species"] is None:
                continue
            for species in spot_data["fish_species"]:
                all_species.add(species)
    all_species.add("NA")
    # Initialize the new format
    new_format = {}
    for county_name, county_data in json_data.items():
        new_format[county_name] = {}
        for species in all_species:
            new_format[county_name][species] = {}

        for spot_name, spot_data in county_data.items():
            if spot_data["fish_species"] is None:
                new_format[county_name]["NA"][spot_name] = {
                    "size": spot_data["size"],
                    "max_depth": spot_data["max_depth"],
                    "rating": spot_data["rating"],
                    "latitude": spot_data["latitude"],
                    "longitude": spot_data["longitude"]
                }
                continue
            for species in spot_data["fish_species"]:
                new_format[county_name][species][spot_name] = {
                    "size": spot_data["size"],
                    "max_depth": spot_data["max_depth"],
                    "rating": spot_data["rating"],
                    "latitude": spot_data["latitude"],
                    "longitude": spot_data["longitude"]
                }

    return new_format


with open('lake_data.json', 'r') as f:
    json_data = json.load(f)

converted_data = convert_json_format(json_data)


with open('lake_data_new.json', 'w') as f:
    f.write(json.dumps(converted_data, indent=4))

