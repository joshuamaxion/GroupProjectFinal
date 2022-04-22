import urllib.request, json
import random
from dotenv import load_dotenv,find_dotenv
import os
from flask import Flask
load_dotenv(find_dotenv())

# Configure API request
app = Flask(__name__)

#key = os.getenv('key')    #local variable

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['key']  #heroku
key = app.config['SQLALCHEMY_DATABASE_URI']

def get_park_data(state_id):
    endpoint = "https://developer.nps.gov/api/v1/parks?stateCode=" + state_id +"&api_key=" + key
    req = urllib.request.Request(endpoint)
    response = urllib.request.urlopen(req).read()
    data = json.loads(response.decode('utf-8'))
    #print(response)
    #print(data)
    for park in data["data"]:
        name = park["fullName"]
        link = park["url"]
        state = park["addresses"][0]["stateCode"]
        desc = park["description"]
        directions = park["directionsUrl"]
        hours = park["operatingHours"][0]["standardHours"]
        coord = park["latLong"]
        coord = "".join(coord)
        return (name, link, state, desc, directions, hours ,coord)

