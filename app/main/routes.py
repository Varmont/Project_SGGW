from flask import Blueprint, render_template, request, session
from ..trips.trip import Trip
from ..extensions import db
from .forms import SearchForm, TripForm

main = Blueprint('main', __name__, template_folder='templates')

@main.route("/", methods=['GET', 'POST'])
def index():
    # executing database
    trips = db.session.execute(db.select(Trip)).scalars()  # basic trips

    # ----------------------FILTER CITIES --------------------------------------------

    # querying database by cities, assigning CityForm and
    form = TripForm()  # dodaję instancję formularza do filtrowania
    cities = []  # docelowo array wszystkich miast
    countries = []  # array wszystkich unikalnych krajów
    # query of cities
    tripsv2 = db.session.query(Trip.city).distinct().all()  # array wszystkich miast jako sqlalchemy obj
    tripsv3 = db.session.query(Trip.country).distinct().all()  # array krajów jako sqlalchemy obj
    tripsfiltered = Trip.query  # instancja sqlalchemy
    for item in tripsv2:
        cities.append(item.__getitem__(0))  # got the array of all cities in the database
    for item in tripsv3:
        countries.append(item.__getitem__(0))
    # passing to choice on website
    form.country.choices = countries
    form.city.choices = cities  # podanie do wyboru wszystkich możliwych miast ze słownika do formularza

    # jeżeli potwierdzono formularz to filtruj dane
    if request.method == 'POST' and form.validate_on_submit():
        filtereddatacity = form.city.data
        filtereddatacountry = form.country.data
        filtereddataprice = request.form["slider"]  # reading data from slider

        tripsfiltered = tripsfiltered.filter(Trip.city == filtereddatacity,
                                             Trip.country == filtereddatacountry,
                                             Trip.price <= filtereddataprice)
        # sort by name
        tripsfiltered = tripsfiltered.order_by(Trip.name).all()
        return render_template('index.html', trips=tripsfiltered, form=form)
    # jeżeli nie, to zwróć basicowe
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

        trips = trips.filter((Trip.name.contains(searcheddata)) |
                             (Trip.city.contains(searcheddata)) |
                             (Trip.country.contains(searcheddata)) |
                             (Trip.description.contains(searcheddata))
                             )
        # sort by name
        trips = trips.order_by(Trip.name).all()

        # if found, show search html with found trips
        if len(trips) > 0:
            return render_template("search.html", form=searchform, searched=searcheddata, trips=trips)

    return render_template('index.html', trips=trips)  # dorobić nie znaleziono takiej wycieczki html
