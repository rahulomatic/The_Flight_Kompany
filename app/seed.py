import random
from datetime import datetime, timedelta, time
from faker import Faker
from .database import SessionLocal, engine, Base
from .models import Flight

fake = Faker()

def random_time_between(start_hour=6, end_hour=23):
    hour = random.randint(start_hour, end_hour)
    minute = random.choice([0, 15, 30, 45])
    return time(hour, minute)

def create_sample_flights(n=200):
    Session = SessionLocal()
    airports = ["BLR","DEL","MAA","BOM","HYD","BLR","COK","CCU","AMD","GOI"]
    airlines = ["Indigo","AirIndia","Vistara","SpiceJet","GoAir"]
    base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for i in range(n):
        origin, destination = random.sample(airports, 2)
        days_offset = random.randint(0, 30)
        dep_date = base_date + timedelta(days=days_offset)
        dep_time = random_time_between()
        departure = datetime.combine(dep_date, dep_time)
        duration_hours = random.randint(1, 5)
        arrival = departure + timedelta(hours=duration_hours, minutes=random.choice([0, 15, 30, 45]))
        price = round(random.uniform(1500, 15000), 2)
        seats_total = random.choice([120, 150, 180])
        seats_available = random.randint(0, seats_total)

        f = Flight(
            airline=random.choice(airlines),
            flight_number=f"AI{random.randint(100,999)}",
            origin=origin,
            destination=destination,
            departure=departure,
            arrival=arrival,
            price=price,
            seats_total=seats_total,
            seats_available=seats_available
        )
        Session.add(f)

        if i % 50 == 0:
            Session.commit()
    Session.commit()
    Session.close()
    print("Seeded", n, "flights")

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    create_sample_flights(500)