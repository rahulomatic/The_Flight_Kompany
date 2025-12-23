import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Flight, Booking
from .pricing import calculate_dynamic_price
import random

def create_booking(db: Session, booking_data):
    """
    Transaction-safe booking
    """

    payment_success = random.choice([True, True, False])

    if not payment_success:
        raise HTTPException(status_code=402, detail="Payment failed")

    # 1️⃣ Lock flight row
    flight = (
        db.query(Flight)
        .filter(Flight.id == booking_data.flight_id)
        .with_for_update()   # 👈 CRITICAL
        .first()
    )

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    if flight.seats_available < booking_data.seats:
        raise HTTPException(status_code=400, detail="Not enough seats")

    # 2️⃣ Calculate price (locked at booking time)
    price_per_seat = calculate_dynamic_price(flight)
    total_price = price_per_seat * booking_data.seats

    # 3️⃣ Reduce seats
    flight.seats_available -= booking_data.seats

    # 4️⃣ Create booking
    booking = Booking(
        pnr=str(uuid.uuid4())[:8].upper(),
        flight_id=flight.id,
        seats_booked=booking_data.seats,
        passenger_name=booking_data.passenger_name,
        passenger_email=booking_data.passenger_email,
        total_price=total_price,
        status="CONFIRMED"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking
