from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalRangeField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


class TripForm(FlaskForm):
    city = SelectField('city', choices=[])

    price = DecimalRangeField('price')

    submit = SubmitField("Submit")


# class PriceForm(FlaskForm):
#     pricesearched = FloatField('pricesearched', validators=[DataRequired()])
#     submit = SubmitField("Submit")
