from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired
from wtforms.widgets.core import HiddenInput


class BookForm(FlaskForm):
    book_id = IntegerField(widget=HiddenInput())
    szerzo = StringField('Szerző', [InputRequired(message='Ez a mező kötelezően kitöltendő.')])
    cim = StringField('Cím', [InputRequired(message='Ez a mező kötelezően kitöltendő.')])