from datetime import datetime
from flask import Flask
from pytz import timezone
from timezonefinder import TimezoneFinder
from sunnyday import Weather
from random import uniform
from folium import Marker
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
import os

app = Flask(__name__)
API_KEY = os.getenv('API_KEY') 
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['API_KEY']
#API_KEY = app.config['SQLALCHEMY_DATABASE_URI']

class Geopoint(Marker):
    
    def __init__(self, latitude, longitude, popup = None):
        super().__init__(location = [latitude, longitude], popup = popup)
        self.latitude = latitude
        self.longitude = longitude
        
    def closest_parallel(self):
        return round(self.latitude)
    
    def get_time(self):
        timezone_string = TimezoneFinder().timezone_at(lat = self.latitude, lng = self.longitude)
        time_now = datetime.now(timezone(timezone_string))
        return time_now
    
    def get_weather(self):
        weather = Weather(API_KEY, lat = self.latitude, lon = self.longitude)
        return weather.next_12h_simplified()
    
    
    @classmethod
    def random(cls):
        return cls(latitude = uniform(-90, 90) , longitude = uniform(-180, 190))
    