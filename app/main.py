from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from typing import List, Optional
from datetime import datetime
from .simulated_feed import router as feed_router

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

@app.get("/search/", response_model=List[schemas.FlightOut])
def search(
    origin: Optional[str] = Query(None, min_length=3, max_length=5),
    destination: Optional[str] = Query(None, min_length=3, max_length=5),
    date: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    sort_by: Optional[str] = Query(None, regex="^(price|duration)$"),
    sort_dir: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    skip: int = 0,
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    if origin:
        origin = origin.upper()
    if destination:
        destination = destination.upper()

 
    date_from = None
    date_to_val = date_to
    if date and not date_to:

        date_only = date.date()
        date_from = datetime.combine(date_only, datetime.min.time())
        date_to_val = datetime.combine(date_only, datetime.max.time())
    elif date:
        date_from = date

    results = crud.search_flights(
        db,
        origin=origin,
        destination=destination,
        date_from=date_from,
        date_to=date_to_val,
        sort_by=sort_by,
        sort_dir=sort_dir,
        skip=skip,
        limit=limit,
    )
    return results
