from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = ""
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config.from_object("config")
db = SQLAlchemy(app)

from app.admin.views import admin as admin_mod
from app.blog.views import blog as blog_mod
from app.posts.views import posts as posts_mod
from app.trips.views import trips as trips_mod

app.register_blueprint(admin_mod)
app.register_blueprint(blog_mod)
app.register_blueprint(posts_mod)
app.register_blueprint(trips_mod)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

@app.route("/")
def home():
    return render_template(url_for("blog.main"))
