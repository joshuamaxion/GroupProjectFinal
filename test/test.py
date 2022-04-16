from flask import Flask
from geo import Geopoint
import folium

app = Flask(__name__)


@app.route('/')
def index():

    #Get latitude and longitude values
    locations = [[41, -1], [34.554296, -84.250793]]

    #Folium Map Instance
    mymap = folium.Map(location = [40, 2], zoom_start=14)

    for loc in locations:
    
        #Getting locatin names
        #created a geopoint instance
        geopoint = Geopoint(latitude = loc[0], longitude = loc[1])
        forecast = geopoint.get_weather()
        popup_content = f"""
        {forecast[0][0][-8:-6]}h: {round(forecast[0][1])}°F<img src= "http://openweathermap.org/img/wn/{forecast[0][-1]}@2x.png" width = 35>
        <hr style="margin:1px">
        {forecast[1][0][-8:-6]}h: {round(forecast[1][1])}°F<img src= "http://openweathermap.org/img/wn/{forecast[1][-1]}@2x.png" width = 35>
        <hr style="margin:1px">
        {forecast[2][0][-8:-6]}h: {round(forecast[2][1])}°F<img src= "http://openweathermap.org/img/wn/{forecast[2][-1]}@2x.png" width = 35>
        <hr style="margin:1px">
        {forecast[3][0][-8:-6]}h: {round(forecast[3][1])}°F<img src= "http://openweathermap.org/img/wn/{forecast[3][-1]}@2x.png" width = 35>
        <hr style="margin:1px">
        <a href="https://www.w3schools.com/html/html_links.asp">Testing</a>
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