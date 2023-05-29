from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CityForm(FlaskForm):
    city = SelectField('city', choices=[], validators=[DataRequired()])
    submit = SubmitField("Submit")
