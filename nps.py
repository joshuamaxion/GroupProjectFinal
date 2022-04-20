import urllib.request, json

# Configure API request
key = "g6rkpnYy977QuiFD41bZNH3he5KvsCd9dMejFDOg"
state_id = "GA"

def get_park_data(state_id):
    endpoint = "https://developer.nps.gov/api/v1/parks?stateCode=" + state_id +"&api_key=" + key
    req = urllib.request.Request(endpoint)
    response = urllib.request.urlopen(req).read()
    data = json.loads(response.decode('utf-8'))

    for park in data["data"]:
        name = park["fullName"]
        link = park["url"]
        state = park["addresses"][0]["stateCode"]
        desc = park["description"]
        directions = park["directionsUrl"]
        hours = park["operatingHours"][0]["standardHours"]
        coord = park["latLong"]
        return (name, link, state, desc, directions, hours ,coord)


get_park_data(state_id)