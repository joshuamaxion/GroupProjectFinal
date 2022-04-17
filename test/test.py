from flask import Flask
from geo import Geopoint
import folium
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():

    #Get latitude and longitude values
    parks = pd.read_csv('GeorgiaStateParks.csv', encoding='unicode_escape')
    locations = [[33.753376, -84.386445, "Welcome!", "(404) 413-2000", "Click on a marker to find a new<br>Georgia park and check its weather!", "Georgia State University"]]

    #add names and locatins to array
    for index, park in parks.iterrows():
        locations.append([park['Latitude'], park['Longitude'], park['Name'], park['Phone'], park['Address'], park['Name']])

    #Folium Map Instance
    mymap = folium.Map(location = [33.753376, -84.386445], zoom_start=14)

    for loc in locations:
        
        #Getting locatin names
        #created a geopoint instance
        geopoint = Geopoint(latitude = loc[0], longitude = loc[1])
        title = loc[2]
        phone = loc[3]
        address = loc[4]
        link = loc[5].replace(" ","+")
        forecast = geopoint.get_weather()
        popup_content = f"""
        <h4 style="text-align: center";>{title}</h4>
        <h6 style="text-align: center";>{address}</h6>

        <hr style="margin:1px">
        <p style=text-align:center;>{forecast[0][0][-8:-6]}h: {round(forecast[0][1])}°F<img src= "http://openweathermap.org/img/wn/{forecast[0][-1]}@2x.png" width = 35></p>
        <hr style="margin:1px">
        <p style=text-align:center;>{forecast[1][0][-8:-6]}h: {round(forecast[1][1])}°F<img src= "http://openweathermap.org/img/wn/{forecast[1][-1]}@2x.png" width = 35></p>
        <hr style="margin:1px">
        <p style=text-align:center;>{forecast[2][0][-8:-6]}h: {round(forecast[2][1])}°F<img src= "http://openweathermap.org/img/wn/{forecast[2][-1]}@2x.png" width = 35></p>
        <hr style="margin:1px">
        <p style=text-align:center;>{forecast[3][0][-8:-6]}h: {round(forecast[3][1])}°F<img src= "http://openweathermap.org/img/wn/{forecast[3][-1]}@2x.png" width = 35></p>
        <hr style="margin:1px">
        <p style="text-align: center; font-weight: bold;">Need more info?</p>
        <p style="text-align: center; color: #6495ED">{phone}</p>
        <a href="https://www.google.com/search?q={link}" target="_blank"><p style="text-align: center;">Check it out!</p></a>
        """
        #Create Popup object and addit to Geopoint
        popup = folium.Popup(popup_content, max_width=400)
        popup.add_to(geopoint)
        geopoint.add_to(mymap)



    #save as HTML file
    mymap.save("map.html")
    return mymap._repr_html_()



if __name__ == '__main__':
    app.run(debug=True)