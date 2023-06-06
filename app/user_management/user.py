from ..extensions import db
from flask_login import UserMixin

user_trip = db.Table("user_trip",
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('trip_id', db.Integer, db.ForeignKey('trip.id'))
                     )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), nullable=False)
    followed = db.relationship('Trip', secondary=user_trip, backref='follower', lazy='dynamic')

    def is_following(self, tripID):
        return self.followed.filter(user_trip.c.trip_id == tripID).count() > 0
