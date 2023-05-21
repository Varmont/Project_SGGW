from flask import Blueprint, render_template
from ..trips.trip import Trip
from ..extensions import db

main = Blueprint('main', __name__, template_folder = 'templates')

@main.route("/")
def index():
    trips = db.session.execute(db.select(Trip)).scalars()
    return render_template('index.html', trips = trips)