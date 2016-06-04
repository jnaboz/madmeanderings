from flask import render_template, Blueprint, url_for

posts = Blueprint("posts", __name__, url_prefix="/posts")

@posts.route("/")
def main():
    return render_template("posts/main.html")
