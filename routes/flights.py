from flask import Blueprint, render_template, request
from flask_login import login_required
from models.flight import Flight
from pricing import calculate_dynamic_price
from datetime import datetime
from flask import jsonify, request
from datetime import datetime








flights_bp = Blueprint("flights", __name__)

from datetime import datetime

def parse_departure_time(time_str):
    try:
        return datetime.strptime(time_str, "%I:%M %p")
    except ValueError:
        return datetime.strptime(time_str, "%H:%M %p")


@flights_bp.route("/search", methods=["GET", "POST"])
@login_required
def search_flights():
    flights = []

    source = request.form.get("source")
    destination = request.form.get("destination")

    date_str = request.form.get("date")
    if date_str:
        search_date = datetime.strptime(date_str, "%Y-%m-%d").date()


    
    search_date = None

    if date_str:
        search_date = datetime.strptime(date_str, "%Y-%m-%d").date()


    if request.method == "POST":
        source = request.form["source"]
        destination = request.form["destination"]

        flights = Flight.query.filter_by(
            source=source,
            destination=destination
        ).all()

        for flight in flights:
            flight.dynamic_price =  flight.get_dynamic_price()


    return render_template("search.html", flights=flights)

@flights_bp.route("/api/flights", methods=["GET"])
def api_get_all_flights():
    flights = Flight.query.all()
    return jsonify([flight_to_dict(f) for f in flights])

@flights_bp.route("/api/search", methods=["GET"])
def api_search_flights():
    source = request.args.get("source")
    destination = request.args.get("destination")
    sort_by = request.args.get("sort")  # price | seats

    query = Flight.query
    date_str = request.args.get("date")

    if date_str:
        search_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        query = query.filter_by(departure_date=search_date)


    if source:
        query = query.filter_by(source=source)

    if destination:
        query = query.filter_by(destination=destination)

    if search_date:
        query = query.filter_by(departure_date=search_date)

    flights = query.all()



    # Sorting
    if sort_by == "price":
        flights.sort(key=lambda f: f.get_dynamic_price())
    elif sort_by == "seats":
        flights.sort(key=lambda f: f.available_seats, reverse=True)

    return jsonify([flight_to_dict(f) for f in flights])


def flight_to_dict(flight):
    return {
        "id": flight.id,
        "flight_number": flight.flight_number,
        "source": flight.source,
        "destination": flight.destination,
        "departure_time": flight.departure_time,
        "base_fare": flight.base_fare,
        "dynamic_price": flight.get_dynamic_price(),
        "available_seats": flight.available_seats,
        "total_seats": flight.total_seats,
        "pricing_tier": flight.pricing_tier,
        "demand_level": flight.demand_level
    }
