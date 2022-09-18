from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, URL


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class AddCafeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Img URL", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    seats = StringField("Number of seats")
    has_wifi = BooleanField("Is there wifi available?", default=False)
    has_sockets = BooleanField("Ample power sockets", default=False)
    has_toilet = BooleanField("Is there a restroom?", default=False)
    can_take_calls = BooleanField("Can you take calls?", default=False)
    coffee_price = StringField("Coffee price", validators=[DataRequired()])
    submit = SubmitField("Submit")
