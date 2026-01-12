from flask import Blueprint, render_template, request
from flask_login import login_required
from models.flight import Flight

flights_bp = Blueprint("flights", __name__)

@flights_bp.route("/search", methods=["GET", "POST"])
@login_required
def search_flights():
    flights = []

    if request.method == "POST":
        source = request.form["source"]
        destination = request.form["destination"]

        flights = Flight.query.filter_by(
            source=source,
            destination=destination
        ).all()

    return render_template("search.html", flights=flights)
