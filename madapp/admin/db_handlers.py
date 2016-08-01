from config import ALLOWED_EXTENSIONS, UPLOADED_IMAGES_DEST
from flask import request
from flask_security.utils import encrypt_password
from madapp import db, app, user_datastore
from madapp.models import User, Role, Photo, ScaledPhoto, Post, Trip, Comment
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os


def add_role(form):
    role = Role(form.name.data, form.description.data)
    try:
        db.session.add(role)
        db.session.commit()
    except IntegrityError:
        pass


def add_trip(form):
    trip = Trip(form.location.data, form.start_date.data,
                form.end_date.data, form.cover.data)
    try:
        db.session.add(trip)
        db.session.commit()
    except IntegrityError:
        pass


def add_user(form):
    user_roles = []
    for role in map(int, form.roles.data):
        r = Role.query.filter_by(id=role).first()
        if r is not None:
            user_roles.append(r)
    user = User(form.name.data, form.email.data,
                encrypt_password(form.password.data), user_roles)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        pass


def submit_post(form):
    post = Post(form.title.data, form.trip.data, form.content.data)
    try:
        db.session.add(post)
        db.session.commit()
    except IntegrityError:
        pass


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_photo(form):
    # if user does not select file, browser also
    # submit a empty part without filename
    filename = secure_filename(form.image.data.filename)
    if filename:
        form.image.data.save(os.path.join(UPLOADED_IMAGES_DEST, filename))
        photo = Photo(filename, form.description.data)
        sphoto = ScaledPhoto(photo.id, 0, 0, 1)
        db.session.add(photo)
        db.session.add(sphoto)
        db.session.commit()
    else:
        pass


DBHandlers = {
    "photos": upload_photo,
    "posts": submit_post,
    "roles": add_role,
    "trips": add_trip,
    "users": add_user,
}
