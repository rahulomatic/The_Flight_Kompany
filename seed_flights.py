from app import create_app
from extensions import db
from models.flight import Flight

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
            price=4200,
            total_seats=180,
            available_seats=180
        ),
        Flight(
            flight_number="AI 101",
            source="BOM",
            destination="DEL",
            departure_time="02:15 PM",
            price=5100,
            total_seats=150,
            available_seats=150
        ),
        Flight(
            flight_number="SG 404",
            source="DEL",
            destination="BLR",
            departure_time="06:45 PM",
            price=4800,
            total_seats=160,
            available_seats=160
        )
    ]

    db.session.add_all(flights)
    db.session.commit()

    print("Flights added successfully")
