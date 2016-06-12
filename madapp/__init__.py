from flask import Flask, render_template, redirect, url_for
from flask_admin import Admin, helpers
from flask_sqlalchemy import SQLAlchemy
from flask_security import (SQLAlchemyUserDatastore, Security)

app = Flask(__name__)
app.secret_key = ""
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config.from_object("config")
db = SQLAlchemy(app)

fadmin = Admin(app, name="Mad Meanderings", template_mode="bootstrap3")

from madapp import models
from madapp.admin.views import admin_bp as admin_mod
#import madapp.admin.views
from madapp.blog.views import blog_bp as blog_mod
from madapp.posts.views import posts_bp as posts_mod
from madapp.trips.views import trips_bp as trips_mod

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(admin_base_template=fadmin.base_template,
                admin_view=fadmin.index_view,
                h=helpers)

app.register_blueprint(admin_mod)
app.register_blueprint(blog_mod)
app.register_blueprint(posts_mod)
app.register_blueprint(trips_mod)

@app.route("/")
def home():
    return render_template(url_for("blog.main"))
