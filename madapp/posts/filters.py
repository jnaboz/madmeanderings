from madapp import app
from madapp.models import Trip


def get_post_trip_location(post):
    tid = post.trip
    trip = Trip.query.filter_by(id=tid).first()
    return trip.location

app.jinja_env.filters["get_post_trip_location"] = get_post_trip_location
