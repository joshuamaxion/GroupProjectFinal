import folium
import pandas as pd

parks = pd.read_csv('GeorgiaStateParks.csv', encoding='unicode_escape')
#view the dataset
print(parks.head())

home = [34.554296, -84.250793]
map = folium.Map(location=home, zoom_start=8)

for index, park in parks.iterrows():
    location = [park['Latitude'], park['Longitude']]
    folium.Marker(location, popup = f'Name:{park["Name"]}').add_to(map)
    
locations = []

for index, park in parks.iterrows():
    locations.append([park['Latitude'],park['Longitude']])

print(locations)
# save map to html file
map.save('index.html')