from extensions import db


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(50), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    