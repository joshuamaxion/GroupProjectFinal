import flask
from flask_login import login_user, current_user, LoginManager, logout_user
from flask_login.utils import login_required
import os

app = flask.Flask(__name__)

Data_url=os.getenv("DataBase")
if Data_url.startswith("postgres://"):
    Data_url = Data_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = Data_url
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = "login"
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
    
@app.route("/")
def index():
    return flask.render_template("index.html",)


@app.route("/signup", methods=["POST"])
def signup_post():
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        pass
    else:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    return flask.redirect(flask.url_for("login"))

    
@app.route("/login", methods=["POST"])
def login_post():
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return flask.redirect(flask.url_for("index"))

    else:
        return flask.jsonify({"status": 401, "reason": "Username or Password Error"})



app.run(host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True)