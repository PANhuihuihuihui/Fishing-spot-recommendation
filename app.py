from flask import Flask, render_template, request, jsonify
from tree import buildTree
import json
from functools import lru_cache

app = Flask(__name__)

# Load and convert JSON data
with open('./data/lake_data_new.json') as f:
    json_data = json.load(f)

tree = buildTree(json_data)


def find_counties(tree):
    res_list = []
    for county in tree.children:
        res ={
            "name": county.name,
        }
        res_list.append(res)
    return res_list
@lru_cache(maxsize=32)
def find_species(tree, county_name):
    for county in tree.children:
        if county.name == county_name:
            res_list = []
            for species in county.children:
                res = {
                    "name": species.name,
                }
                res_list.append(res)
            res_list.append({"name": "All"})
            return sorted(res_list, key=lambda k: k['name'])
    return []
@lru_cache(maxsize=32)
def find_fishing_spots(tree, county_name, species_name):
    for county in tree.children:
        if county.name == county_name:
            for species in county.children:
                if species_name == "All":
                    res_list = []
                    for spot in species.children:
                        res = {
                            "name": spot.name,
                            "size": spot.size,
                            "max_depth": spot.max_depth,
                            "rating": spot.rating,
                            "latitude": spot.latitude,
                            "longitude": spot.longitude

                        }
                        res_list.append(res)
                    return res_list
                if species.name == species_name:
                    res_list = []
                    for spot in species.children:
                        res = {
                            "name": spot.name,
                            "size": spot.size,
                            "max_depth": spot.max_depth,
                            "rating": spot.rating,
                            "latitude": spot.latitude,
                            "longitude": spot.longitude

                        }
                        res_list.append(res)
                    return res_list
    return []

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/counties')
def counties():
    results = find_counties(tree)
    return jsonify(results)

@app.route('/species_by_county')
def fishing_spots_by_county():
    county = request.args.get('query')
    species_list = find_species(tree, county)
    return jsonify(species_list)

@app.route('/fishing_spots_by_county_and_species')
def fishing_spots_by_county_and_species():
    county = request.args.get('county')
    species = request.args.get('species')
    fishing_spots = find_fishing_spots(tree, county, species)
    return jsonify(fishing_spots)

if __name__ == '__main__':
    
    app.run(debug=True)
   
