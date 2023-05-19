from .trip import Trip
from ..extensions import db
from datetime import datetime
from flask import Blueprint, render_template, request, url_for, redirect

trips = Blueprint('trips', __name__, template_folder = 'templates')

@trips.route('/tripadd', methods=['GET', 'POST'])
def tripadd():
    if request.method == 'POST':
        name = request.form['name']
        date_start = datetime.strptime(request.form['date_start'], '%Y-%m-%d').date()
        date_end = datetime.strptime(request.form['date_end'], '%Y-%m-%d').date()
        city = request.form['city']
        price = request.form['price']
        description = request.form['description']
        trip = Trip(name=name, date_start=date_start, date_end=date_end, city=city, price=price, description=description)
        db.session.add(trip)
        db.session.commit()
        return render_template('tripsite.html', name=name, date_start=date_start, date_end=date_end, city=city, price=price, description=description)
    return render_template('tripadd.html')

@trips.route('/trip/<tripID>', methods = ['GET', 'POST'])
def tripview(tripID):
    trip = db.session.execute(db.select(Trip).where(Trip.id == tripID)).scalar()
    return render_template('tripsite.html', name=trip.name, date_start=trip.date_start, date_end=trip.date_end, city=trip.city, price=trip.price, description=trip.description)