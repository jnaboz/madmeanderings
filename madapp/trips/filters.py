from madapp import app
from madapp.models import Photo
import os


def get_photo_filename(photo_id):
    filename = Photo.query.filter_by(id=photo_id).first().filename
    return os.path.join("uploads", filename)


app.jinja_env.filters["get_photo_filename"] = get_photo_filename
