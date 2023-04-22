# SI 507: Final Project

Fishing spot recommendation system in MI

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites

Ensure you have the following software installed on your system:
you could use requirements.txt to install all the packages you need

- Python 3.8+
- pip (Python package installer)
- selenium
- flask
- BeautifulSoup

### Installing

Follow these steps to set up a local development environment:

1. Clone the repository:
2. install all the packages you need
```bash
conda install -r requirements.txt
```
3. collect data
```bash
cd data
python link_data_collection.py
python location_collection.py
python data_process.py

```
Notice: you have to repalce the google map api key in  `location_collection.py` with your own key. And
after these steps, you will get the data file name `lake_data_new.json` you need in the data folder

3. Run the application:
```bash
flask app.py
```
