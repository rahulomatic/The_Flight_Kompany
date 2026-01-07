from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import BookingCreate, BookingResponse
from ..booking_service import create_booking
from ..models import Booking
from fastapi import HTTPException


router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
def book_flight(data: BookingCreate, db: Session = Depends(get_db)):
    booking = create_booking(db, data)
    return booking


@router.get("/{pnr}", response_model=BookingResponse)
def get_booking(pnr: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("/{pnr}/cancel")
def cancel_booking(pnr: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status == "CANCELLED":
        return {"message": "Already cancelled"}

    booking.status = "CANCELLED"
    booking.flight.seats_available += booking.seats_booked

    db.commit()
    return {"message": "Booking cancelled"}

@router.get("/bookings/{pnr}/receipt")
def get_booking_receipt(pnr: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return {
        "pnr": booking.pnr,
        "flight_id": booking.flight_id,
        "passenger_name": booking.passenger_name,
        "seat_number": booking.seat_number,
        "price": booking.price,
        "status": booking.status,
        "created_at": booking.created_at
    }
