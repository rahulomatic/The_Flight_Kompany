from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.flight import Flight
from models.booking import Booking
from extensions import db
from flask import abort
from pricing import calculate_dynamic_price
from datetime import datetime


bookings_bp = Blueprint("bookings", __name__)

@bookings_bp.route("/book/<int:flight_id>", methods=["GET", "POST"])
@login_required
def book_flight(flight_id):
    flight = Flight.query.get_or_404(flight_id)

    if request.method == "POST":
        selected_seat = request.form["seat"]

        # 🔒 prevent double booking
        existing = Booking.query.filter_by(
            flight_id=flight.id,
            seat_number=selected_seat
        ).first()
        if existing:
            return "Seat already booked"

        # 💰 FREEZE PRICE AT BOOKING TIME (THIS IS THE KEY)
        booking_price = flight.get_dynamic_price()


        booking = Booking(
            user_id=current_user.id,
            flight_id=flight.id,
            passenger_name=request.form["name"],
            seat_number=selected_seat,
            price=booking_price      # ✅ STORED HERE
        )

        flight.available_seats -= 1

        db.session.add(booking)
        db.session.commit()

        return redirect(url_for("bookings.my_bookings"))


    # GET request → show seat map
    booked_seats = [
        b.seat_number for b in
        Booking.query.filter_by(flight_id=flight.id).all()
    ]

    return render_template(
        "book.html",
        flight=flight,
        booked_seats=booked_seats,
        price = calculate_dynamic_price(
            base_fare=flight.base_fare,
            available_seats=flight.available_seats,
            total_seats=flight.total_seats,
            departure_time=flight.departure_time,
            demand_level="medium",
            pricing_tier=flight.pricing_tier
        )


    )



@bookings_bp.route("/my-bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    flights = {f.id: f for f in Flight.query.all()}

    return render_template(
        "my_bookings.html",
        bookings=bookings,
        flights=flights
    )

@bookings_bp.route("/cancel/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    # 🔒 Security: only owner can cancel
    if booking.user_id != current_user.id:
        abort(403)

    flight = Flight.query.get(booking.flight_id)

    # Restore seat count
    flight.available_seats += 1

    db.session.delete(booking)
    db.session.commit()

    return redirect(url_for("bookings.my_bookings"))

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from io import BytesIO
from flask import send_file

@bookings_bp.route("/ticket/<int:booking_id>")
@login_required
def download_ticket(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    # 🔒 Security check
    if booking.user_id != current_user.id:
        abort(403)

    flight = Flight.query.get(booking.flight_id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>The Flight Kompany</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"<b>Booking ID:</b> TFK-{booking.id}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Passenger:</b> {booking.passenger_name}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Flight:</b> {flight.flight_number}", styles["Normal"]))
    elements.append(Paragraph(
        f"<b>Route:</b> {flight.source} → {flight.destination}",
        styles["Normal"]
    ))
    elements.append(Paragraph(f"<b>Departure:</b> {flight.departure_time}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Seat:</b> {booking.seat_number}", styles["Normal"]))
    elements.append(
    Paragraph(f"<b>Price:</b> ₹{booking.price}", styles["Normal"])
)

    elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph(
        "Please arrive at the airport at least 2 hours before departure.",
        styles["Italic"]
    ))

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"ticket_TFK_{booking.id}.pdf",
        mimetype="application/pdf"
    )
