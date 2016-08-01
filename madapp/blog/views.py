from flask import render_template, Blueprint, url_for
from madapp.models import Trip, Post

blog_bp = Blueprint("blog_bp", __name__, url_prefix=None)

@blog_bp.route("/")
def main():
    trips = Trip.query.order_by(Trip.id.desc())[:10]
    posts = Post.query.order_by(Post.id.desc())[:10]
    return render_template("blog/main.html",
                           recent_trips=trips,
                           recent_posts=posts)

@blog_bp.route("/about")
def about():
    return render_template("blog/about.html")
