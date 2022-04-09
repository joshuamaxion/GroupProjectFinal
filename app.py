from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import random
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())


# PROD configs
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['HEROKU_POSTGRESQL_GOLD_URL']    #use this for Heroku
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DBCONNECTION']    #use this for Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')     # local test
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DBCONNECTION']
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DBCONNECTION']
#app.permanent_session_lifetime = timedelta(days=5) 
#s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#TokenTimer = 300

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
    if (existingUser or existingEmail):
        return True
    return False

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

@app.route("/info", methods = ["POST","GET"])
def info():

    return render_template("map.html")

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
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    print(getAllUsers())
    #port = int(os.environ.get('PORT', 7000))
    app.run(debug=True, port = 8080)
    #app.run(debug=True, port = 8000)