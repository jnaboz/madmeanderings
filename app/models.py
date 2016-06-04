from app import db
from sqlalchemy_utils.types.choice import ChoiceType


POST_STATES = {
    "DR": "Draft",
    "PU": "Published",
}


class User(db.Model):
    __tablename__ = "users"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)


class Post(db.Model):
    __tablename__ = "posts"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    post_date = db.Column(db.DateTime())
    modified_date = db.Column(db.DateTime())
    state = db.Column(ChoiceType(POST_STATES))
    tags = db.Column(db.String(100))
    trip = db.Column(db.Integer, db.ForeignKey("trip.id"))


class Trip(db.Model):
    __tablename__ = "trips"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship("Post")


class Comment(db.Model):
    __tablename__ = "comments"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    #post = db.relationship()


class Photo(db.Model):
    __tablename__ = "photos"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)


class ScaledPhoto(db.Model):
    __tablename__ = "scaledphotos"
    __bind_key__ = "blogdb"
