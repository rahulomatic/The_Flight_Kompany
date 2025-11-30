from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import Index
from .database import Base
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    airline = Column(String, nullable=False)
    flight_number = Column(String, nullable=False, index=True)
    origin = Column(String, nullable=False, index=True)
    destination = Column(String, nullable=False, index=True)
    departure = Column(DateTime, nullable=False, index=True)
    arrival = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    seats_total = Column(Integer, nullable=False)
    seats_available = Column(Integer, nullable=False)

    # FIX: You MUST add this or SQLAlchemy throws "no property 'bookings'"
    bookings = relationship("Booking", back_populates="flight")

    # FIX: For pricing history
    pricing_history = relationship("PricingHistory", back_populates="flight")

    __table_args__ = (
        Index('idx_od_departure', "origin", "destination", "departure"),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    bookings = relationship("Booking", back_populates="user")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))
    seats_booked = Column(Integer)
    booking_status = Column(String, default="PENDING")
    booking_time = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    flight = relationship("Flight", back_populates="bookings")

    payment = relationship("Payment", back_populates="booking", uselist=False)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    amount = Column(Float)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    booking = relationship("Booking", back_populates="payment")


class DynamicPricingRule(Base):
    __tablename__ = "pricing_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String)
    rule_type = Column(String)
    factor = Column(Float)
    is_active = Column(Boolean, default=True)


class PricingHistory(Base):
    __tablename__ = "pricing_history"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id"))
    old_price = Column(Float)
    new_price = Column(Float)
    changed_at = Column(DateTime, default=datetime.utcnow)
    reason = Column(String)

    # FIXED: relationship name must match property in Flight
    flight = relationship("Flight", back_populates="pricing_history")