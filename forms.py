from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email



class RegisterForm(FlaskForm):
    """Form for registering a user."""
    username = StringField("Username", validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired()], render_kw={"placeholder": "Password"})
    email = StringField("Email", validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    first_name = StringField("First Name", validators=[InputRequired()], render_kw={"placeholder": "First name"})
    last_name = StringField("Last Name", validators=[InputRequired()], render_kw={"placeholder": "Last name"})


class LoginForm(FlaskForm):
    """Form for registering a user."""
    username = StringField("Username", validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired()], render_kw={"placeholder": "Password"})


class SearchName(FlaskForm):
    """Search by Drink Name"""
    name = StringField("Search by Drink Name", validators=[InputRequired()], render_kw={"placeholder": "Search for a Drink"})

class SearchIng(FlaskForm):
    """Search by Drink Name""" 
    name = StringField("Search by Ingredient")
