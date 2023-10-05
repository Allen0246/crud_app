from flask_wtf import FlaskForm
from wtforms import PasswordField, IntegerField, StringField
from wtforms.validators import InputRequired 
from wtforms.widgets.core import HiddenInput


class LoginForm(FlaskForm):
    user_id = IntegerField(widget=HiddenInput())
    username = StringField('Felhasználónév', [InputRequired(message='Ez a mező kötelezően kitöltendő.')])
    password = PasswordField('Jelszó', [InputRequired(message='Ez a mező kötelezően kitöltendő.')])
