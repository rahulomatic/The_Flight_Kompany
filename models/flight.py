from extensions import db
from pricing import calculate_dynamic_price
from datetime import date



class Flight(db.Model):
    __tablename__ = "flight"

    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(10), nullable=False)
    destination = db.Column(db.String(10), nullable=False)
    departure_time = db.Column(db.String(20), nullable=False)

    departure_date = db.Column(db.Date, nullable=False, default=date.today)

    base_fare = db.Column(db.Integer, nullable=False)
    pricing_tier = db.Column(db.String(20), default="economy")

    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)

    demand_level = db.Column(db.String(20), default="medium")

    # ✅ OPTION A — THIS METHOD
    def get_dynamic_price(self):
        return calculate_dynamic_price(
            base_fare=self.base_fare,
            available_seats=self.available_seats,
            total_seats=self.total_seats,
            departure_time=self.departure_time,
            demand_level=self.demand_level,
            pricing_tier=self.pricing_tier
        )