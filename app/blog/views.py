from flask import render_template, Blueprint, url_for

blog = Blueprint("blog", __name__, url_prefix=None)

@blog.route("/")
def main():
    return render_template("blog/main.html")

@blog.route("/about")
def about():
    return render_template("blog/about.html")
