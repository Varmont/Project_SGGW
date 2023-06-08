from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


class TripForm(FlaskForm):
    city = SelectField('city', choices=[])
    country = SelectField('city', choices=[])
    price = HiddenField('price')
    submit = SubmitField("Submit")


