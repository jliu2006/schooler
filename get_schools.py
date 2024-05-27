import overpy
from geopy.geocoders import Nominatim
import ssl

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
            'latitude': node.lat,
            'longitude': node.lon,
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

    for school in schools:
        print(f"Name: {school['name']}")
        print(f"Location: ({school['latitude']}, {school['longitude']})")
        location = geolocator.reverse(f"{school['latitude']}, {school['longitude']}")
        if location:
            school['address'] = location.address
        print(f"Address: {school['address']}")
        print()
else:
    print("Address not found.")