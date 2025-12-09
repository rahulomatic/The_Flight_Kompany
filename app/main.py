from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from typing import List, Optional
from datetime import datetime
from .simulated_feed import router as feed_router
import asyncio
from . import simulator
from .pricing import calculate_dynamic_price
from .models import Flight
from .simulator import scheduler_loop
import asyncio



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flight Search API - Milestone 1")
app.include_router(feed_router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/flights/", response_model=schemas.FlightOut)
def create_flight(f: schemas.FlightCreate, db: Session = Depends(get_db)):
    return crud.create_flight(db, f)

@app.get("/flights/", response_model=List[schemas.FlightOut])
def list_all_flights(skip: int = 0, limit: int = Query(100, le=500), db: Session = Depends(get_db)):
    return crud.list_flights(db, skip=skip, limit=limit)

@app.get("/search_flights")
def search_flights(origin: str, destination: str, db: Session = Depends(get_db)):

    flights = db.query(Flight).filter(
        Flight.origin == origin,
        Flight.destination == destination
    ).all()

    results = []

    for f in flights:

        dynamic_price = calculate_dynamic_price(
            base_fare=f.price,
            seats_available=f.seats_available,
            seats_total=f.seats_total,
            departure=f.departure,
            airline_tier="standard"
        )

        results.append({
            "id": f.id,
            "airline": f.airline,
            "flight_number": f.flight_number,
            "origin": f.origin,
            "destination": f.destination,
            "departure": f.departure,
            "arrival": f.arrival,
            "seats_available": f.seats_available,
            "total_seats": f.seats_total,
            "base_price": f.price,
            "dynamic_price": dynamic_price
        })

    return results


@app.on_event("startup")
async def startup_event():
    # start background simulation task
    # run with a longer interval for dev (e.g., every 60 seconds)
    asyncio.create_task(simulator.scheduler_loop(interval_seconds=60))

# inside endpoint or after query results