from .trip import Trip
from ..user_management.user import user_trip
from ..extensions import db
from datetime import datetime
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import current_user
from ..main.forms import CityForm

trips = Blueprint('trips', __name__, template_folder = 'templates')

@trips.route('/tripadd', methods=['GET', 'POST'])
def tripadd():
    if request.method == 'POST':
        name = request.form['name']
        date_start = datetime.strptime(request.form['date_start'], '%Y-%m-%d').date()
        date_end = datetime.strptime(request.form['date_end'], '%Y-%m-%d').date()
        country = request.form['country']
        city = request.form['city']
        price = request.form['price']
        description = request.form['description']
        image = request.form['image']
        trip = Trip(name=name, country=country, date_start=date_start, date_end=date_end, city=city,
                    price=price, description=description, image=image)
        db.session.add(trip)
        db.session.commit()
        return render_template('tripsite.html', trip=trip)
    return render_template('tripadd.html')

@trips.route('/trip?trip=<tripID>', methods = ['GET', 'POST'])
def tripview(tripID):
    #trip = db.session.execute(db.select(Trip).where(Trip.id == tripID)).scalar()
    trip = Trip.query.filter_by(id=tripID).first()
    return render_template('tripsite.html', trip=trip)

@trips.route('/follow?trip=<tripID>', methods=['GET', 'POST'])
def follow(tripID):
    if current_user.is_authenticated:
        if current_user.is_following(tripID):
            trip = Trip.query.filter_by(id=tripID).first()
            flash("Ta wycieczka jest już dodana do ulubionych.", "error")
            return render_template('tripsite.html', trip=trip)
        trip = Trip.query.filter_by(id=tripID).first()
        current_user.followed.append(trip)
        db.session.commit()
        flash('Dodano wycieczkę do ulubionych.', 'mess')
        return redirect(url_for('trips.tripview', tripID=tripID))
    else:
        flash("Musisz być zalogowany, aby dodać wycieczkę do ulubionych!", 'error')
        return render_template('login.html')

@trips.route('/unfollow?trip=<tripID>', methods=['GET', 'POST'])
def unfollow(tripID):
    trip = Trip.query.filter_by(id=tripID).first()
    current_user.followed.remove(trip)
    db.session.commit()
    flash('Usunięto wycieczkę z ulubionych.', 'mess')
    return redirect(url_for('trips.tripview', tripID=tripID))


@trips.route('/favourites', methods=['GET'])
def favourite():
    userID = request.args.get('user')
    form = CityForm()
    trips = db.session.execute(db.select(Trip).join(user_trip).where(user_trip.c.user_id == userID)).scalars()

    return render_template('favourites.html', trips=trips, form=form)

