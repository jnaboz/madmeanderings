from flask import render_template, Blueprint, url_for

trips_bp = Blueprint('trips_bp', __name__, url_prefix='/trips')

@trips_bp.route("/")
def main():
    return render_template("trips/main.html")
