import overpy
from geopy.geocoders import Nominatim
import ssl
import json
from decimal import Decimal

ssl._create_default_https_context = ssl._create_unverified_context
geolocator = Nominatim(user_agent="schooler")

def find_schools_osm(latitude, longitude, radius):
    api = overpy.Overpass()

    # json query
    query = f"""
    [out:json];
    node
      ["amenity"="school"]
      (around:{radius},{latitude},{longitude});
    out body;
    """

    result = api.query(query)

    schools = []
    for node in result.nodes:
        school = {
            'name': node.tags.get('name', 'N/A'),
            'latitude': float(node.lat),     # decimal to float so that results can be stored as JSON file
            'longitude': float(node.lon), 
            'address': node.tags.get('addr:full', 'N/A')
        }
        schools.append(school)

    return schools

address = "1600 Amphitheatre Parkway, Mountain View, CA"
location = geolocator.geocode(address)
if location:
    latitude, longitude = location.latitude, location.longitude
    radius = 5000  # 5 km

    schools = find_schools_osm(latitude, longitude, radius)

    # Save to JSON
    file_path = "school_results.json"
    with open(file_path, "w") as file:
        json.dump(schools, file, indent=4, default=str)  # Use default=str to handle Decimals

    print(f"Search results saved to {file_path}")
    print()

    # Print results
    for school in schools:
        print(f"Name: {school['name']}")
        print(f"Location: ({school['latitude']}, {school['longitude']})")
        print(f"Address: {school['address']}")
        print()
else:
    print("Address not found.")