from flask import render_template, Blueprint, url_for

trips = Blueprint('trips', __name__, url_prefix='/trips')

@trips.route("/")
def main():
    return render_template("trips/main.html")
