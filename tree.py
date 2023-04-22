class Tree():
    def __init__(self, name, children=None):
        self.name  = name
        self.children = children if children else []
    def add_child(self, child):
        self.children.append(child)
    def __str__(self):
        return self.name

class County(Tree):
    def __init__(self, name, children=None):
        super().__init__(name, children)

class FishingSpot(Tree):
    def __init__(self, name, county, size, max_depth, rating, latitude, longitude):
        super().__init__(name, [])
        self.county = county
        self.size = size
        self.max_depth = max_depth
        self.rating = rating
        self.latitude = latitude
        self.longitude = longitude

class Species(Tree):
    def __init__(self, name, children=None):
        #def __init__(self, name, image_url, link, fishing, identification, identification_href, diet, life_history, background_info):
        super().__init__(name, children)
        # self.image_url = image_url
        # self.link = link
        # self.fishing = fishing
        # self.identification = identification
        # self.identification_href = identification_href
        # self.diet = diet
        # self.life_history = life_history
        # self.background_info = background_info


def buildTree(json_data):
    root = Tree("Root", [])

    for county_name, species_data in json_data.items():
        county_node = County(county_name, [])
        root.add_child(county_node)

        for species_name, spot_data in species_data.items():
            species_node = Species(species_name, [])
            county_node.add_child(species_node)

            for spot_name, details in spot_data.items():
                fishing_spot_node = FishingSpot(
                    name=spot_name,
                    county=county_name,
                    size=details["size"],
                    max_depth=details["max_depth"],
                    rating=details["rating"],
                    latitude=details["latitude"],
                    longitude=details["longitude"]
                )
                species_node.add_child(fishing_spot_node)

    return root

# converted_data = convert_json_format(json_data)
# tree = buildTree(converted_data)
