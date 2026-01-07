import requests
from .database import SessionLocal, Base, engine
from .models import Flight
from datetime import datetime
import dateutil.parser

def ingest(url="http://localhost:8000/external_feed/sample?count=50"):
    resp = requests.get(url)
    data = resp.json()
    Session = SessionLocal()
    for f in data["flights"]:
        departure = dateutil.parser.isoparse(f["departure"])
        arrival = dateutil.parser.isoparse(f["arrival"])
        flight = Flight(
            airline=f["airline"],
            flight_number=f["flight_number"],
            origin=f["origin"],
            destination=f["destination"],
            departure=departure,
            arrival=arrival,
            price=f["price"],
            seats_total=f["seats_total"],
            seats_available=f["seats_available"],
        )
        Session.add(flight)
    Session.commit()
    Session.close()
