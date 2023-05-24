from flask import Blueprint, render_template, request
from ..trips.trip import Trip
from ..extensions import db
from .searchform import SearchForm

main = Blueprint('main', __name__, template_folder='templates')


@main.route("/filterwindow")
def filterwindow():
    return render_template('filterwindow.html')

@main.route("/")
def index():
    trips = db.session.execute(db.select(Trip)).scalars()
    return render_template('index.html', trips=trips)

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
    form = SearchForm()
    trips = Trip.query
    if request.method == 'POST' and form.validate_on_submit():
        # get data from submitted form
        searcheddata = form.searched.data
        # query the database

        trips = trips.filter(Trip.name.contains(searcheddata) |
                             Trip.city.contains(searcheddata) |
                             Trip.description.contains(searcheddata)
                             )
        # sort by name
        trips = trips.order_by(Trip.name).all()

        # if found, show search html with found trips
        if len(trips) > 0:
            return render_template("search.html", form=form, searched=searcheddata, trips=trips)

    return render_template('index.html', trips=trips)  # dorobić nie znaleziono takiej wycieczki html
