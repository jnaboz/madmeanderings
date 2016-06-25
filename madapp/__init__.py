from flask import Flask, render_template, redirect, url_for
from flask_admin import helpers
from flask_sqlalchemy import SQLAlchemy
from flask_security import (SQLAlchemyUserDatastore, Security)
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads
from flaskext.markdown import Markdown

app = Flask(__name__)
app.secret_key = ""
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config.from_object("config")
db = SQLAlchemy(app)
Markdown(app)

IMAGE_SET = UploadSet("images", IMAGES)
configure_uploads(app, (IMAGE_SET,))

from madapp import models
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

from madapp.admin.views import admin_bp as admin_mod
from madapp.blog.views import blog_bp as blog_mod
from madapp.posts.views import posts_bp as posts_mod
from madapp.trips.views import trips_bp as trips_mod

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(admin_base_template="admin/index.html",
                admin_view="admin/index.html",
                h=helpers)

app.register_blueprint(admin_mod)
app.register_blueprint(blog_mod)
app.register_blueprint(posts_mod)
app.register_blueprint(trips_mod)


@app.route("/")
def home():
    return render_template(url_for("blog.main"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
