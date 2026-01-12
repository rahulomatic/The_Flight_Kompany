from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models.flight import Flight
from models.booking import Booking
from extensions import db
from utils import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
@login_required
def admin_dashboard():
    admin_required()
    flights = Flight.query.all()
    bookings = Booking.query.all()
    return render_template(
        "admin/dashboard.html",
        flights=flights,
        bookings=bookings
    )


@admin_bp.route("/admin/add-flight", methods=["POST"])
@login_required
def add_flight():
    admin_required()

    flight = Flight(
        flight_number=request.form["flight_number"],
        source=request.form["source"],
        destination=request.form["destination"],
        departure_time=request.form["departure_time"],
        price=int(request.form["price"]),
        total_seats=int(request.form["seats"]),
        available_seats=int(request.form["seats"])
    )

    db.session.add(flight)
    db.session.commit()

    return redirect(url_for("admin.admin_dashboard"))
