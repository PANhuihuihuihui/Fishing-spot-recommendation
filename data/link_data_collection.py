import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


text = "link='/michigan-lakes/alcona-county/352/'/><entity id='003' link='/michigan-lakes/alger-county/353/'/><entity id='005' link='/michigan-lakes/allegan-county/354/'/><entity id='007' link='/michigan-lakes/alpena-county/355/'/><entity id='009' link='/michigan-lakes/antrim-county/356/'/><entity id='011' link='/michigan-lakes/arenac-county/357/'/><entity id='013' link='/michigan-lakes/baraga-county/358/'/><entity id='015' link='/michigan-lakes/barry-county/359/'/><entity id='017' link='/michigan-lakes/bay-county/360/'/><entity id='019' link='/michigan-lakes/benzie-county/361/'/><entity id='021' link='/michigan-lakes/berrien-county/362/'/><entity id='023' link='/michigan-lakes/branch-county/363/'/><entity id='025' link='/michigan-lakes/calhoun-county/364/'/><entity id='027' link='/michigan-lakes/cass-county/365/'/><entity id='029' link='/michigan-lakes/charlevoix-county/366/'/><entity id='031' link='/michigan-lakes/cheboygan-county/367/'/><entity id='033' link='/michigan-lakes/chippewa-county/368/'/><entity id='035' link='/michigan-lakes/clare-county/369/'/><entity id='037' link='/michigan-lakes/clinton-county/370/'/><entity id='039' link='/michigan-lakes/crawford-county/371/'/><entity id='041' link='/michigan-lakes/delta-county/372/'/><entity id='043' link='/michigan-lakes/dickinson-county/373/'/><entity id='045' link='/michigan-lakes/eaton-county/374/'/><entity id='047' link='/michigan-lakes/emmet-county/375/'/><entity id='049' link='/michigan-lakes/genesee-county/376/'/><entity id='051' link='/michigan-lakes/gladwin-county/377/'/><entity id='053' link='/michigan-lakes/gogebic-county/378/'/><entity id='055' link='/michigan-lakes/grand-traverse-county/379/'/><entity id='057' link='/michigan-lakes/gratiot-county/380/'/><entity id='059' link='/michigan-lakes/hillsdale-county/381/'/><entity id='061' link='/michigan-lakes/houghton-county/382/'/><entity id='063' link='/michigan-lakes/huron-county/383/'/><entity id='065' link='/michigan-lakes/ingham-county/384/'/><entity id='067' link='/michigan-lakes/ionia-county/385/'/><entity id='069' link='/michigan-lakes/iosco-county/386/'/><entity id='071' link='/michigan-lakes/iron-county/387/'/><entity id='073' link='/michigan-lakes/isabella-county/388/'/><entity id='075' link='/michigan-lakes/jackson-county/389/'/><entity id='077' link='/michigan-lakes/kalamazoo-county/390/'/><entity id='079' link='/michigan-lakes/kalkaska-county/391/'/><entity id='081' link='/michigan-lakes/kent-county/392/'/><entity id='083' link='/michigan-lakes/keweenaw-county/393/'/><entity id='085' link='/michigan-lakes/lake-county/394/'/><entity id='087' link='/michigan-lakes/lapeer-county/395/'/><entity id='089' link='/michigan-lakes/leelanau-county/396/'/><entity id='091' link='/michigan-lakes/lenawee-county/397/'/><entity id='093' link='/michigan-lakes/livingston-county/398/'/><entity id='095' link='/michigan-lakes/luce-county/399/'/><entity id='097' link='/michigan-lakes/mackinac-county/400/'/><entity id='099' link='/michigan-lakes/macomb-county/401/'/><entity id='101' link='/michigan-lakes/manistee-county/402/'/><entity id='103' link='/michigan-lakes/marquette-county/403/'/><entity id='105' link='/michigan-lakes/mason-county/404/'/><entity id='107' link='/michigan-lakes/mecosta-county/405/'/><entity id='109' link='/michigan-lakes/menominee-county/406/'/><entity id='111' link='/michigan-lakes/midland-county/407/'/><entity id='113' link='/michigan-lakes/missaukee-county/408/'/><entity id='115' link='/michigan-lakes/monroe-county/409/'/><entity id='117' link='/michigan-lakes/montcalm-county/410/'/><entity id='119' link='/michigan-lakes/montmorency-county/411/'/><entity id='121' link='/michigan-lakes/muskegon-county/412/'/><entity id='123' link='/michigan-lakes/newaygo-county/413/'/><entity id='125' link='/michigan-lakes/oakland-county/414/'/><entity id='127' link='/michigan-lakes/oceana-county/415/'/><entity id='129' link='/michigan-lakes/ogemaw-county/416/'/><entity id='131' link='/michigan-lakes/ontonagon-county/417/'/><entity id='133' link='/michigan-lakes/osceola-county/418/'/><entity id='135' link='/michigan-lakes/oscoda-county/419/'/><entity id='137' link='/michigan-lakes/otsego-county/420/'/><entity id='139' link='/michigan-lakes/ottawa-county/421/'/><entity id='141' link='/michigan-lakes/presque-isle-county/422/'/><entity id='143' link='/michigan-lakes/roscommon-county/423/'/><entity id='145' link='/michigan-lakes/saginaw-county/424/'/><entity id='151' link='/michigan-lakes/sanilac-county/425/'/><entity id='153' link='/michigan-lakes/schoolcraft-county/426/'/><entity id='155' link='/michigan-lakes/shiawassee-county/427/'/><entity id='147' link='/michigan-lakes/st-clair-county/1809/'/><entity id='149' link='/michigan-lakes/st-joseph-county/1810/'/><entity id='147' link='/michigan-lakes/st-clair-county/428/'/><entity id='149' link='/michigan-lakes/st-joseph-county/429/'/><entity id='157' link='/michigan-lakes/tuscola-county/430/'/><entity id='159' link='/michigan-lakes/van-buren-county/431/'/><entity id='161' link='/michigan-lakes/washtenaw-county/432/'/><entity id='163' link='/michigan-lakes/wayne-county/433/'/><entity id='165' link='/michigan-lakes/wexford-county/434/'"
prefix = "https://www.lake-link.com"

links = re.findall(r"link='(.*?)'", text)
full_links = [prefix + link for link in links]
lake_info_by_county = {}
for link in full_links:
    lakes_info = {}
    # Set up the Selenium webdriver
    driver = webdriver.Chrome()
    driver.get(link)

    # Wait for the JavaScript elements to load
    try:
        wait = WebDriverWait(driver, 10)
        lake_elems = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.map-tile-image")))
    except TimeoutException:
        print("Timed out waiting for page to load", link)
        driver.quit()
        continue

    # Get the page source and parse it with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    county_name = soup.find("h1").get_text().strip()
    county_name = re.sub(r"\sCounty Lakes", "", county_name)
    county_lakes = soup.find_all('div', class_='col')
    for lake_card, lake_elem in zip(county_lakes, lake_elems):
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
        lat = float(lake_elem.get_attribute("data-lat"))
        lng = float(lake_elem.get_attribute("data-lng"))
        lakes_info[name]['lat'] = lat
        lakes_info[name]['lng'] = lng

        lakes_info[name]['size'] = size
        lakes_info[name]['max_depth'] = max_depth
        lakes_info[name]['rating'] = float(rating['alt'].split()[0]) if rating else 0.0
        fish_species_list = lake_card.find('ul', class_='fish-species').find_all('li')
        if fish_species_list:
            lakes_info[name]['fish_species'] = [species.text.strip() for species in fish_species_list]
        else:
            lakes_info[name]['fish_species'] = None
    lake_info_by_county[county_name] = lakes_info

    # If there are no lakes
    if not lake_elements:
        print("No lakes found.")
    driver.quit()

with open('lake_data.json', 'w') as outfile:
    json.dump(lake_info_by_county, outfile,indent=4)

# Close the webdriver

