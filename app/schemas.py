from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FlightBase(BaseModel):
    airline: str
    flight_number: str
    origin: str = Field(..., min_length=3, max_length=5)
    destination: str = Field(..., min_length=3, max_length=5)
    departure: datetime
    arrival: datetime
    price: float = Field(..., ge=0)
    seats_total: int = Field(..., ge=0)
    seats_available: int = Field(..., ge=0)

class FlightCreate(FlightBase):
    pass

class FlightOut(BaseModel):
    id: int
    airline: str
    flight_number: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    price: float
    seats_total: int
    seats_available: int

    class Config:
        orm_mode = True
