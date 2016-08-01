from madapp.models import Post, Trip
import madapp.posts.filters
from flask import render_template, Blueprint, url_for

posts_bp = Blueprint("posts_bp", __name__, url_prefix="/posts")


@posts_bp.route("/")
def main():
    posts = Post.query.order_by(Post.id.desc())[:10]
    return render_template("posts/main.html",
                           posts=posts)


@posts_bp.route("/<pid>")
def show_post(pid):
    post_data = Post.query.filter_by(id=pid).first()
    if post_data is None:
        abort(404)
    return render_template("posts/post.html", post_data=post_data)
