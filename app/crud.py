from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import select, desc, asc
from datetime import datetime, timedelta

def create_flight(db: Session, flight: schemas.FlightCreate):
    db_f = models.Flight(**flight.dict())
    db.add(db_f)
    db.commit()
    db.refresh(db_f)
    return db_f

def get_flight(db: Session, flight_id: int):
    return db.query(models.Flight).filter(models.Flight.id == flight_id).first()

def list_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flight).offset(skip).limit(limit).all()

def search_flights(
    db: Session,
    origin: str = None,
    destination: str = None,
    date_from: datetime = None,
    date_to: datetime = None,
    sort_by: str = None,
    sort_dir: str = "asc",
    skip: int = 0,
    limit: int = 50,
):
    q = db.query(models.Flight)

    if origin:
        q = q.filter(models.Flight.origin == origin.upper())
    if destination:
        q = q.filter(models.Flight.destination == destination.upper())
    if date_from:
        q = q.filter(models.Flight.departure >= date_from)
    if date_to:
        q = q.filter(models.Flight.departure <= date_to)

    if sort_by == "price":
        order = asc(models.Flight.price) if sort_dir == "asc" else desc(models.Flight.price)
        q = q.order_by(order)
    elif sort_by == "duration":
        from sqlalchemy import (func,)
        duration_expr = func.strftime('%s', models.Flight.arrival) - func.strftime('%s', models.Flight.departure)
        order = asc(duration_expr) if sort_dir == "asc" else desc(duration_expr)
        q = q.order_by(order)
    else:
        q = q.order_by(models.Flight.departure)
        

    return q.offset(skip).limit(limit).all()


def update_flight_price(db: Session, flight: models.Flight, new_price: float, reason: str = ""):
    # update the flight price and optionally create a pricing history record
    old_price = flight.price
    flight.price = float(new_price)
    db.add(flight)
    # add pricing history
    ph = models.PricingHistory(
        flight_id=flight.id,
        old_price=old_price,
        new_price=new_price,
        changed_at=datetime.utcnow(),
        reason=reason[:255]
    )
    db.add(ph)
    db.commit()
    db.refresh(flight)
    return flight

def get_all_flights_for_simulation(db: Session):
    # return flights we want to simulate (you can filter by upcoming dates)
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    soon = now + timedelta(days=60)  # simulate flights within next 60 days
    return db.query(models.Flight).filter(models.Flight.departure <= soon).all()