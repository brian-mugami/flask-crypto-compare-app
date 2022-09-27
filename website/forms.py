from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField,StringField
from wtforms.validators import DataRequired
from .models import Crypto



class AddForm(FlaskForm):
    name = StringField("Crypto to compare ", validators=[DataRequired()])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):

    name = StringField("Crypto-Name", validators=[DataRequired()])
    submit = SubmitField("Submit")