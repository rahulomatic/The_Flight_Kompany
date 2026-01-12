from app import create_app
from extensions import db
from models.flight import Flight
from datetime import date, timedelta

app = create_app()

with app.app_context():
    if Flight.query.first():
        print("Flights already exist")
        exit()

    flights = [
    Flight(
        flight_number="6E 203",
        source="BOM",
        destination="DEL",
        departure_time="10:30 AM",
        departure_date=date.today() + timedelta(days=1),
        base_fare=4200,
        pricing_tier="economy",
        demand_level="medium",
        total_seats=180,
        available_seats=180
    ),
    Flight(
        flight_number="AI 101",
        source="BOM",
        destination="DEL",
        departure_time="14:15 PM",
        departure_date=date.today() + timedelta(days=1),
        base_fare=5100,
        demand_level="medium",
        pricing_tier="premium",
        total_seats=150,
        available_seats=150
    ),
    Flight(
        flight_number="SG 404",
        source="DEL",
        destination="BLR",
        departure_time="18:45 PM",
        base_fare=4800,
        demand_level="medium",
        pricing_tier="economy",
        total_seats=160,
        available_seats=160
    )
]


    db.session.add_all(flights)
    db.session.commit()

    print("Flights added successfully")
