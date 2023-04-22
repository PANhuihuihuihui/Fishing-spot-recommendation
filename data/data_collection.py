import requests
from bs4 import BeautifulSoup
import re
import json

def has_multiple_species(section):
    species_count = len(section.find_all('h2'))
    return species_count > 1
def extract_species_info(species_section):
    # Extract the information under the 'h3' headings for a single species
    headers = species_section.find_all(lambda tag: tag.name in ['h3', 'h4'])
    properties = {}
    if len(headers) == 0:
        print("No headers", str(species_section.prettify()))
    for header in headers:
        property_name = header.text.strip().lower().replace(':', '')
        if property_name == '' or property_name == 'management':
            continue
        property_value = ''
        property_href = header.find_next_sibling('p').find('a')
        while header.find_next_sibling('p') is not None:
            header = header.find_next_sibling('p')
            property_value += header.get_text()
        properties[property_name] = property_value
        if property_name == "identification":
            property_href = property_href['href'] if property_href else ''
            properties[property_name + '_href'] = property_href
    return properties

def species():
    print("collecting fish species...")
    url = "https://www.michigan.gov/dnr/education/michigan-species/fish-species"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    fish_species = []

    fish_divs = soup.find_all('div', class_='col-12 col-md-6 col-lg-4')
    
    for fish_div in fish_divs:
        fish_name = fish_div.find('h3').text.strip()
        fish_image_url = fish_div.find('div', class_='topics-promo__section-img')['style'].split("'")[1]
        fish_link = fish_div.find('a', class_='img-link')['href']
        
        
        fish_link = "https://www.michigan.gov/"+fish_link
        response = requests.get(fish_link)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        field_content_div  = soup.find('div', {'class': 'field-content'})

        if has_multiple_species(field_content_div):
            print("Multiple species", fish_link)
            species_sections = field_content_div.find_all('h2')
            for species_section in species_sections:
                species_name = species_section.get_text()
                if species_name == '' or species_name == '\u00a0':
                    continue
                print(species_name)
                

                fish_details = extract_species_info(field_content_div)


                fish_species.append({
                    'name': species_name,
                    'image_url': fish_image_url,
                    'link': fish_link,
                    'details': fish_details
                })
        else:
            fish_details = extract_species_info(field_content_div)

            fish_species.append({
                'name': fish_name,
                'image_url': fish_image_url,
                'link': fish_link,
                'details': fish_details
            })
    return fish_species
        


def safeToEat():
    print("collecting safe to eat...")
    safeToEat = []
    # specify the URL of the web page

    with open("/Users/pan/Documents/course/SI507/FinalProject/data/safeEating1.html", "r") as f:
        # Read the contents of the file into a string variable
        html = f.read()

    # parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # locate the table element by its ID
    table = soup.find('table', {'id': 'DataTables_Table_0'})

    # get all the rows in the table body
    rows = table.find_all('tr')[1:]
    print(len(rows))

    # iterate over the rows and extract the data
    for row in rows:
        cols = row.find_all('td')
        region = cols[0].text.strip()
        county = cols[1].text.strip()
        waterbody = cols[2].text.strip()
        fish_type = cols[3].text.strip()
        chem_of_concern = cols[4].text.strip()
        size = cols[5].text.strip()
        servings = cols[6].text.strip()
        safeToEat_dic = {
            "region": region,
            "county": county,
            "waterbody": waterbody,
            "fish_type": fish_type,
            "chem_of_concern": chem_of_concern,
            "size": size,
            "servings": servings
        }
        safeToEat.append(safeToEat_dic)
        # do something with the data, such as save it to a file or a database
        # print(region, county, waterbody, fish_type, chem_of_concern, size, servings)
    with open("/Users/pan/Documents/course/SI507/FinalProject/data/safeEating2.html", "r") as f:
        # Read the contents of the file into a string variable
        html = f.read()

    # parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # locate the table element by its ID
    table = soup.find('table', {'id': 'DataTables_Table_0'})

    # get all the rows in the table body
    rows = table.find_all('tr')[1:]
    print(len(rows))

    # iterate over the rows and extract the data
    for row in rows:
        cols = row.find_all('td')
        region = cols[0].text.strip()
        county = cols[1].text.strip()
        waterbody = cols[2].text.strip()
        fish_type = cols[3].text.strip()
        chem_of_concern = cols[4].text.strip()
        size = cols[5].text.strip()
        servings = cols[6].text.strip()
        safeToEat_dic = {
            "region": region,
            "county": county,
            "waterbody": waterbody,
            "fish_type": fish_type,
            "chem_of_concern": chem_of_concern,
            "size": size,
            "servings": servings
        }
        safeToEat.append(safeToEat_dic)
    return safeToEat


def counties():
    url = "https://www.michigan.gov/dnr/things-to-do/fishing/where/inland-lake-maps-list"
    page = requests.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')
    map = soup.find('map', id='FPMap0')

    counties = []

    # Loop over the county links and areas
    if map is not None:
        county_areas = map.find_all('area')
        for link in county_areas:
            # Get the county name from the link text or alt text
            county_name = link.get('alt').split(' ')[0]
            # Get the county link URL
            county_link = link.get('href')
            # Get the county coordinates if the link is an image map area
            county_coords = link['coords']
            counties.append({
                'name': county_name,
                'url': county_link,
                'coordinates': county_coords
            })
            if county_link == "":
                print(county_name)
    # print(len(counties))
    # print(counties)
    return counties

def lakeByCounty():
    url = "https://www.michigan.gov/dnr/things-to-do/fishing/where/inland-lake-maps-list"
    page = requests.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')
    map = soup.find('map', id='FPMap0')
    # Loop over the county links and areas
    # Create a dictionary to store the lake information by county name
    lake_info_by_county = {}

    county_areas = map.find_all('area')
    for link in county_areas:
        # Get the county link URL
        county_link = link.get('href')
        county_name = link.get('alt').split(' ')[0]
        if county_link is None or county_link == "" :
            continue
        county_link = "https://www.michigan.gov"+county_link
        # print(county_link)
        response = requests.get(county_link)
        soup = BeautifulSoup(response.content, 'html.parser')
        lake_div = soup.find('div', class_='field-content')
        lake_links = lake_div.find_all('a')
        lake_info = {}
        for a in lake_links:
            lake_name = a.text.strip()
            lake_url = a['href']
            lake_info[lake_name] = lake_url
            print(lake_info)

        lake_info_by_county[county_name] = lake_info
        # print(lake_info_by_county[county_name])

    # print(lake_info_by_county)
    return lake_info_by_county


def lakeByCountyLink():

    text = "link='/michigan-lakes/alcona-county/352/'/><entity id='003' link='/michigan-lakes/alger-county/353/'/><entity id='005' link='/michigan-lakes/allegan-county/354/'/><entity id='007' link='/michigan-lakes/alpena-county/355/'/><entity id='009' link='/michigan-lakes/antrim-county/356/'/><entity id='011' link='/michigan-lakes/arenac-county/357/'/><entity id='013' link='/michigan-lakes/baraga-county/358/'/><entity id='015' link='/michigan-lakes/barry-county/359/'/><entity id='017' link='/michigan-lakes/bay-county/360/'/><entity id='019' link='/michigan-lakes/benzie-county/361/'/><entity id='021' link='/michigan-lakes/berrien-county/362/'/><entity id='023' link='/michigan-lakes/branch-county/363/'/><entity id='025' link='/michigan-lakes/calhoun-county/364/'/><entity id='027' link='/michigan-lakes/cass-county/365/'/><entity id='029' link='/michigan-lakes/charlevoix-county/366/'/><entity id='031' link='/michigan-lakes/cheboygan-county/367/'/><entity id='033' link='/michigan-lakes/chippewa-county/368/'/><entity id='035' link='/michigan-lakes/clare-county/369/'/><entity id='037' link='/michigan-lakes/clinton-county/370/'/><entity id='039' link='/michigan-lakes/crawford-county/371/'/><entity id='041' link='/michigan-lakes/delta-county/372/'/><entity id='043' link='/michigan-lakes/dickinson-county/373/'/><entity id='045' link='/michigan-lakes/eaton-county/374/'/><entity id='047' link='/michigan-lakes/emmet-county/375/'/><entity id='049' link='/michigan-lakes/genesee-county/376/'/><entity id='051' link='/michigan-lakes/gladwin-county/377/'/><entity id='053' link='/michigan-lakes/gogebic-county/378/'/><entity id='055' link='/michigan-lakes/grand-traverse-county/379/'/><entity id='057' link='/michigan-lakes/gratiot-county/380/'/><entity id='059' link='/michigan-lakes/hillsdale-county/381/'/><entity id='061' link='/michigan-lakes/houghton-county/382/'/><entity id='063' link='/michigan-lakes/huron-county/383/'/><entity id='065' link='/michigan-lakes/ingham-county/384/'/><entity id='067' link='/michigan-lakes/ionia-county/385/'/><entity id='069' link='/michigan-lakes/iosco-county/386/'/><entity id='071' link='/michigan-lakes/iron-county/387/'/><entity id='073' link='/michigan-lakes/isabella-county/388/'/><entity id='075' link='/michigan-lakes/jackson-county/389/'/><entity id='077' link='/michigan-lakes/kalamazoo-county/390/'/><entity id='079' link='/michigan-lakes/kalkaska-county/391/'/><entity id='081' link='/michigan-lakes/kent-county/392/'/><entity id='083' link='/michigan-lakes/keweenaw-county/393/'/><entity id='085' link='/michigan-lakes/lake-county/394/'/><entity id='087' link='/michigan-lakes/lapeer-county/395/'/><entity id='089' link='/michigan-lakes/leelanau-county/396/'/><entity id='091' link='/michigan-lakes/lenawee-county/397/'/><entity id='093' link='/michigan-lakes/livingston-county/398/'/><entity id='095' link='/michigan-lakes/luce-county/399/'/><entity id='097' link='/michigan-lakes/mackinac-county/400/'/><entity id='099' link='/michigan-lakes/macomb-county/401/'/><entity id='101' link='/michigan-lakes/manistee-county/402/'/><entity id='103' link='/michigan-lakes/marquette-county/403/'/><entity id='105' link='/michigan-lakes/mason-county/404/'/><entity id='107' link='/michigan-lakes/mecosta-county/405/'/><entity id='109' link='/michigan-lakes/menominee-county/406/'/><entity id='111' link='/michigan-lakes/midland-county/407/'/><entity id='113' link='/michigan-lakes/missaukee-county/408/'/><entity id='115' link='/michigan-lakes/monroe-county/409/'/><entity id='117' link='/michigan-lakes/montcalm-county/410/'/><entity id='119' link='/michigan-lakes/montmorency-county/411/'/><entity id='121' link='/michigan-lakes/muskegon-county/412/'/><entity id='123' link='/michigan-lakes/newaygo-county/413/'/><entity id='125' link='/michigan-lakes/oakland-county/414/'/><entity id='127' link='/michigan-lakes/oceana-county/415/'/><entity id='129' link='/michigan-lakes/ogemaw-county/416/'/><entity id='131' link='/michigan-lakes/ontonagon-county/417/'/><entity id='133' link='/michigan-lakes/osceola-county/418/'/><entity id='135' link='/michigan-lakes/oscoda-county/419/'/><entity id='137' link='/michigan-lakes/otsego-county/420/'/><entity id='139' link='/michigan-lakes/ottawa-county/421/'/><entity id='141' link='/michigan-lakes/presque-isle-county/422/'/><entity id='143' link='/michigan-lakes/roscommon-county/423/'/><entity id='145' link='/michigan-lakes/saginaw-county/424/'/><entity id='151' link='/michigan-lakes/sanilac-county/425/'/><entity id='153' link='/michigan-lakes/schoolcraft-county/426/'/><entity id='155' link='/michigan-lakes/shiawassee-county/427/'/><entity id='147' link='/michigan-lakes/st-clair-county/1809/'/><entity id='149' link='/michigan-lakes/st-joseph-county/1810/'/><entity id='147' link='/michigan-lakes/st-clair-county/428/'/><entity id='149' link='/michigan-lakes/st-joseph-county/429/'/><entity id='157' link='/michigan-lakes/tuscola-county/430/'/><entity id='159' link='/michigan-lakes/van-buren-county/431/'/><entity id='161' link='/michigan-lakes/washtenaw-county/432/'/><entity id='163' link='/michigan-lakes/wayne-county/433/'/><entity id='165' link='/michigan-lakes/wexford-county/434/'"
    prefix = "https://www.lake-link.com"

    links = re.findall(r"link='(.*?)'", text)
    full_links = [prefix + link for link in links]
    lake_info_by_county = {}
    for link in full_links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        county_name = soup.find("h1").get_text().strip()
        county_name = re.sub(r"\sCounty Lakes", "", county_name)
        lake_elements = soup.find_all('div', class_='col')
        lakes_info = {}
        for lake_card in lake_elements:
            name = lake_card.find("h5", class_="card-title").get_text().strip()
            if name is None or lake_card is None:
                continue
            lakes_info[name] = {}
            size = None
            max_depth = None
            rating = lake_card.find('img', alt=True, class_='me-2')
            size_depth_list = lake_card.find_all("li")
            for item in size_depth_list:
                if "SIZE" in item.get_text():
                    size = item.find("strong").get_text().strip()
                elif "MAX DEPTH" in item.get_text():
                    max_depth = item.find("strong").get_text().strip()


            lakes_info[name]['size'] = size
            lakes_info[name]['max_depth'] = max_depth
            lakes_info[name]['rating'] = float(rating['alt'].split()[0]) if rating else 0.0
            print(lake_card.prettify())
            
            fish_species_list = lake_card.find('div', class_=['d-flex', 'justify-content-between', 'mt-2'])
            print(fish_species_list.prettify())
            fish_species_list = fish_species_list.find_next('div')
            print(fish_species_list.prettify())
            fish_species_list  = fish_species_list.find('ul', class_='fish-species').find_all('li') if fish_species_list else []
            
            fish_species = [species.text.strip() for species in fish_species_list]
            if len(fish_species) == 0:
                lakes_info[name]['fish_species'] = None
                # print(f"No fish species found for {name}", link)

            else:
                lakes_info[name]['fish_species'] = sp
                print(f"Found fish species for {name}", link)


        lake_info_by_county[county_name] = lakes_info

        # If there are no lakes
        if not lake_elements:
            print("No lakes found.")
    return lake_info_by_county


def save_to_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def create_unique_lake_names(lake_info_by_county):
    unique_lake_by_county = {}
    
    for county, lakes in lake_info_by_county.items():
        unique_lake_by_county[county] = {}
        
        for lake, url in lakes.items():
            unique_name = lake.split(' (')[0]
            
            if unique_name not in unique_lake_by_county[county]:
                unique_lake_by_county[county][unique_name] = {
                    'urls': [url]
                }
            else:
                unique_lake_by_county[county][unique_name]['urls'].append(url)
    
    return unique_lake_by_county


           


if __name__ == "__main__":
    # species = species()
    # save_to_json(species, 'species.json')
    # safeToEat = safeToEat()
    # save_to_json(safeToEat, 'safe_to_eat.json')
    # counties = counties()
    # save_to_json(counties, 'counties.json')
    lake_data = lakeByCountyLink()
    save_to_json(lake_data, 'lake_link.json')
    


"""help me write a fishing spot recommending system base on user's location and wanted spec
"""

"""
give fish species, and fishing lake, find the the species in the same pfd page or not.
also the lake nake should be right above the species name.


https://www.lake-link.com/michigan-lakes/{}-county/352/
https://www.lake-link.com/michigan-lakes/{}-county/434/


""

you have two tasks
1. you are give a long string, extract the link it. and add this "https://www.lake-link.com"in the begining of the link.
2. using python with bs4 to extract informtion from above link. you will be given a example named county_lake. You need to find lake name, fish species name it contains , 
county_lake = {
<div class="col">
    <div class="card h-100 shadow-sm gradient-background-grey-white">
      <div class="card-header bg-primary">
        <h5 class="card-title m-0 p-0 text-white">Ninth Street Pond (Lake Besser)</h5>
      </div>
      <div class="card-body py-0 px-2">
        
        <div class="d-flex justify-content-between mt-2">
          <div>
            <ul class="list-unstyled">
              <li>
                <small class="text-muted mr-2">SIZE:</small>
                <strong>   392 acres</strong>
              </li>
              
                <li>
                  <small class="text-muted">MAX DEPTH:</small>
                  <strong> 23 ft</strong>
                </li>
              
            </ul>
          </div>
          <div>
            <small>
              <ul class="fish-species list-unstyled" data-lake-id="21986"><li>Black Crappie</li><li>Bluegill</li><li>Northern Pike</li><li>Smallmouth Bass</li><li>Walleye</li><li>Yellow Perch</li></ul>
            </small>
          </div>
        </div>
      </div>
      <div class="card-footer text-end border-0 pt-0" style="background-color: transparent;">
        <a class="btn btn-outline-primary btn-sm stretched-link" href="/michigan-lakes/alpena-county-county/ninth-street-pond-lake-besser/21986/" role="button" title="Ninth Street Pond (Lake Besser) - Alpena County County, Michigan">More Details <i class="fad fa-chevron-double-right ms-2"></i>
        </a>
      </div>
    </div>
  </div>
  }

"""