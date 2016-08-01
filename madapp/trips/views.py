from flask import render_template, Blueprint, url_for
import madapp.trips.filters
from madapp.models import Trip

trips_bp = Blueprint('trips_bp', __name__, url_prefix='/trips')

@trips_bp.route("/")
def main():
    trips = Trip.query.order_by(Trip.id.desc())[:10]
    return render_template("trips/main.html",
                           trips=trips)


@trips_bp.route("/<tid>")
def show_trip(tid):
    trip_data = Trip.query.filter_by(id=tid).first()
    if trip_data is None:
        abort(404)
    return render_template("trips/trip.html", trip_data=trip_data)
