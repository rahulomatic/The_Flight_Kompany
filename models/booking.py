from extensions import db
from datetime import datetime

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)
    flight_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)


    passenger_name = db.Column(db.String(100), nullable=False)
    seat_number = db.Column(db.String(5), nullable=False)

    booking_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
