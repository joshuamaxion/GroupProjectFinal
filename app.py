from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from dotenv import load_dotenv,find_dotenv
from sqlalchemy import false
load_dotenv(find_dotenv())
from geo import *
import folium
import pandas as pd
from nps import *

# PROD configs
app = Flask(__name__)


#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['HEROKU_POSTGRESQL_GOLD_URL']    #use this for Heroku    #use this for Heroku

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']    #use this for Heroku
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

#API_KEY = os.getenv('API_KEY')     # local test
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')     # local test
#app.secret_key = 'super secret key'


#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DBCONNECTION']
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DBCONNECTION']
#app.permanent_session_lifetime = timedelta(days=5) 
TokenTimer = 300
db = SQLAlchemy(app)

class Users(db.Model):
    # Users table definition
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}, {self.email}')"


def isExistingUser(username, email):
    # used for the user entry check in the db
    existingUser = Users.query.filter_by(username=username).first()
    existingEmail = Users.query.filter_by(email=email).first()
    if not existingUser:
        return False
    if not existingEmail:
        return False
    return True

def getAllUsers():
    # returns the current users in the table
    return sorted([user.username for user in Users.query.all()])


def addUser(username, email):
    # adds the user to the Users db
    user = Users(username=username,
                 email=email,)
    db.session.add(user)
    db.session.commit()




'''Below are the Functions that interact with frontEnd directly'''

@app.route("/")
def home():
    # main landing page; renders the main page if logged in, login page otherwise.
    return render_template("index.html")

@app.route("/parking", methods = ['POST'])
def parking():
    state_ids = ["GA","FL","TN"]
    state_id = random.choice(state_ids)
    name, link, state, desc, directions, hours ,coord = get_park_data(state_id)

    return render_template("main.html", name = name, link = link,state = state , desc = desc, directions = directions,
    hours = hours, coord = coord)

@app.route('/login', methods = ['GET','POST'])
def login():
    # workflow when 'Log In' is clicked.

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        if (not isExistingUser(username, email)):                   # when the user doesn't exist
            flash("The username does not exist. Please sign up.")
            return render_template("index.html") 
        else:                                                       # when the user does exist
            session.permanent = True
            session["user"] = username
            session["email"] = email
            flash("Login Successful!")
            return redirect(url_for("main"))

    if request.method == "GET":                                     # when landing on this page using GET request
        if "user" in session:                                       # if there is a active session
            flash("Already logged in!")
            return render_template("main.html")
        else:
            flash("Please login.")
            return render_template("index.html")

@app.route("/info",methods = ['GET','POST'])
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


@app.route("/signup", methods=["POST","GET"])
def signup():
    # workflow when 'Sign Up' is clicked.

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]

        if (not isExistingUser(username, email)):                           # if there is no existing user, send a confirmation email.
            session["user"] = username                                      # when the user clicks on the link, the user will be added.
            session["email"] = email

            session["temporary"] = True
            addUser(username,email)
            return redirect(url_for("home"))
        else:                                                               # if username or email already exists
            flash(f"This username or email already exists.", "info")
            return render_template("signup.html")

    elif "user" in session and "temporary" not in session:                  # if there's an active session, redirect them to the main.
            flash("Already logged in!")
            return render_template("main.html")
    else:
        return render_template("signup.html")                               # when landing on this page using GET request


@app.route("/redirectToMain", methods=["POST","GET"])
def redirectToMain():
    # used for the redirection to prevent unwanted Form submission.
    return redirect(url_for("main"))

@app.route("/showDashboard", methods=["POST","GET"])
def redirectMainGetRequest():
    # This handles the GET request for the main page.
    return render_template("main.html" )
    
@app.route("/main", methods=["POST","GET"])
def main():
    # main page where the queue display will happen.
    #if "user" in session:
        #user = session["user"]
        #currentUsers = getAllUsers()
    return render_template("main.html")
    
@app.route("/logout", methods=["GET","POST"])
def logout():
    # logs out the active session by clearing out the session.

    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    session.pop("temporary", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    #db.drop_all()
    db.create_all()
    #print(getAllUsers())
    port = int(os.environ.get('PORT', 7000))
    #app.run(debug=True, port = 8080)
    #app.run(debug=True, port = 8000)
