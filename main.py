from flask import Flask, render_template, redirect, url_for, abort, flash
from flask_bootstrap import Bootstrap
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_gravatar import Gravatar
from forms import RegisterForm, LoginForm, AddCafeForm
from datetime import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


def hash_password(password):
    encrypted_password = generate_password_hash(
        password,
        method='pbkdf2:sha256',
        salt_length=10
    )
    return encrypted_password


def registered_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# USER CLASS
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# Cafe TABLE Configuration
class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


# with app.app_context():
#     db.create_all()


@app.route("/", methods=["GET"])
def home():
    cafes = db.session.query(Cafe).all()
    cafes_nr = len(cafes)
    current_year = datetime.now().year
    return render_template("index.html", all_cafes=cafes, cafes_nr=cafes_nr, current_year=current_year)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("The email you entered has already been registered. Try logging in.")
            return redirect(url_for("login"))
        else:
            new_user = User()
            new_user.email = form.email.data
            new_user.password = hash_password(form.password.data)
            new_user.name = form.name.data
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("home"))

    return render_template("login.html", form=form)


@app.route("/add-cafe", methods=["GET", "POST"])
@registered_only
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        if Cafe.query.filter_by(map_url=form.map_url.data).first():
            flash("This cafe has already been added.")
            return redirect(url_for("home"))
        else:
            new_cafe = Cafe(
                name=form.name.data,
                map_url=form.map_url.data,
                img_url=form.img_url.data,
                location=form.location.data,
                seats=form.seats.data,
                has_wifi=form.has_wifi.data,
                has_sockets=form.has_sockets.data,
                has_toilet=form.has_toilet.data,
                can_take_calls=form.can_take_calls.data,
                coffee_price=form.coffee_price.data
            )
            db.session.add(new_cafe)
            db.session.commit()
            flash("Thank you for your contribution.")
            return redirect(url_for("home"))

    return render_template("add-cafe.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
