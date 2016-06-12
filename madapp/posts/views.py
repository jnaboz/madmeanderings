from madapp.models import Post, Trip
from flask import render_template, Blueprint, url_for

posts_bp = Blueprint("posts_bp", __name__, url_prefix="/posts")


@posts_bp.route("/")
def main():
    return render_template("posts/main.html")


@posts_bp.route("/<pid>")
def show_post(pid):
    post_data = Post.query.filter_by(id=pid).first()
    return render_template("posts/post.html", post_data=post_data)
