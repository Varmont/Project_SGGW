from flask import Blueprint, render_template, request
from ..trips.trip import Trip
from ..extensions import db
from .forms import SearchForm, CityForm
import numpy as np

main = Blueprint('main', __name__, template_folder='templates')


# @main.route("/fetchrecords", methods=[ "POST", "GET"])
# def fetchrecords():
#     form = PriceForm()
#     trips = Trip.query
#     minimum_price = form.min.data
#     print(minimum_price)
#     if request.method == "POST":
#
#
#         print(minimum_price)
#
#         maximum_price = form.max.data
#         print(maximum_price)
#         trips = trips.filter(float(maximum_price) >= Trip.price >= float(minimum_price))
#         trips = trips.order_by(Trip.name).all()
#         # if found, show search html with found trips
#         if len(trips) > 0:
#             return render_template("search.html", form=form,
#                                    minimum_price=minimum_price,
#                                    maximum_price=maximum_price,
#                                    trips=trips)
#
#     return render_template('index.html', trips=trips)  # dorobić nie znaleziono takiej wycieczki html


@main.route("/", methods=['GET', 'POST'])
def index():
    # executing database
    trips = db.session.execute(db.select(Trip)).scalars()

    # ----------------------FILTER CITIES --------------------------------------------

    # querying database by cities, assigning CityForm and
    form = CityForm()
    cities = []
    # query of cities
    tripsv2 = db.session.query(Trip.city).distinct().all()
    tripsfiltered = Trip.query
    for item in tripsv2:
        cities.append(item.__getitem__(0))  # got the array of all cities in the database
    form.city.choices = cities
    if request.method == 'POST':
        filtereddata = form.city.data
        tripsfiltered = tripsfiltered.filter(Trip.city == filtereddata)
        # sort by name
        tripsfiltered = tripsfiltered.order_by(Trip.name).all()
        return render_template('index.html', trips=tripsfiltered, form=form)

    return render_template('index.html', trips=trips, form=form)


@main.route("/about")
def about():
    return render_template('about.html')


@main.route("/contact")
def contact():
    return render_template('contact.html')


# pass stuff to topnavbar.html

@main.context_processor  # passing stuff to a base file
def indexpass():
    form = SearchForm()
    return dict(form=form)


# creating search function

@main.route("/search", methods=['GET', 'POST'])
def search():
    searchform = SearchForm()
    trips = Trip.query
    if request.method == 'POST' and searchform.validate_on_submit():
        # get data from submitted form
        searcheddata = searchform.searched.data
        # query the database

        trips = trips.filter(Trip.name.contains(searcheddata) |
                             Trip.city.contains(searcheddata) |
                             Trip.description.contains(searcheddata)
                             )
        # sort by name
        trips = trips.order_by(Trip.name).all()

        # if found, show search html with found trips
        if len(trips) > 0:
            return render_template("search.html", form=searchform, searched=searcheddata, trips=trips)

    return render_template('index.html', trips=trips)  # dorobić nie znaleziono takiej wycieczki html


