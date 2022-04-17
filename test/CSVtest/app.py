import folium
import pandas as pd

parks = pd.read_csv('Georgia State Parks.csv', encoding='unicode_escape')
#view the dataset
print(parks.head())

home = [34.554296, -84.250793]
map = folium.Map(location=home, zoom_start=8)

for index, park in parks.iterrows():
    location = [park['latitude'], park['longitude']]
    folium.Marker(location, popup = f'Name:{park["store"]}\n Revenue($):{park["revenue"]}').add_to(map_kenya)

# save map to html file
map.save('index.html')