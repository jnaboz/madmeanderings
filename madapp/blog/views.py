from flask import render_template, Blueprint, url_for

blog_bp = Blueprint("blog_bp", __name__, url_prefix=None)

@blog_bp.route("/")
def main():
    return render_template("blog/main.html")

@blog_bp.route("/about")
def about():
    return render_template("blog/about.html")
