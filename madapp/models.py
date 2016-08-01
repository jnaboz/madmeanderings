from flask_security import (UserMixin, RoleMixin)
from madapp import db
from sqlalchemy_utils.types import ChoiceType
import datetime


POST_STATES = {
    "DR": "Draft",
    "PU": "Published",
}

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
    info={"bind_key": "blogdb"}
)


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    """
    User Model

    User information for posters and commenters

    Members:
        ID    - Unique user identifier
        name  - Name of user
        email - Email of user (unique)
    """
    __tablename__ = "user"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String())
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref("users", lazy="dynamic"))

    def __init__(self, name, email, password, roles, active=True):
        self.name = name
        self.email = email
        self.password = password
        self.roles = roles
        self.active = active

    def __repr__(self):
        return self.name


class Post(db.Model):
    """
    Post Model

    Content and photo information for a blog post

    Members:
        ID            - Unique post identifier
        post_date     - Original date when the post was created
        modified_date - Date of the most recent update
        title         - Title of the post
        state         - Post state (draft/published)
        tags          - Keywords for tagging the post
        trip          - Trip that post is associated with
        comments      - List of comments that are associated with the post
        content       - Actual post content
    """
    __tablename__ = "post"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    post_date = db.Column(db.DateTime())
    modified_date = db.Column(db.DateTime())
    title = db.Column(db.String(100))
    state = db.Column(ChoiceType(POST_STATES))
    trip = db.Column(db.Integer, db.ForeignKey("trip.id"))
    comments = db.relationship("Comment")
    content = db.Column(db.String())

    def __init__(self, title, trip, content):
        self.title = title
        self.trip = trip
        self.content = content
        self.post_date = datetime.datetime.now()

    def __repr__(self):
        return self.title


class Trip(db.Model):
    """
    Trip Model
    
    A trip refers to a collection of posts to a specific location or for a
    specific vacation or trip

    Members:
        ID          - Trip unique identifier
        posts       - list of posts that correspond to the trip
        location    - Location of the trip (a.k.a. title)
        start_date  - Beginning of the date range for the trip
        end_date    - End of the date range for the trip
        cover_image - Image to show off the trip
    """
    __tablename__ = "trip"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship("Post", lazy="dynamic")
    location = db.Column(db.String(255), unique=True)
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    cover_image = db.Column(db.Integer, db.ForeignKey("photo.id"))

    def __init__(self, location, start_date, end_date, cover_image):
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.cover_image = cover_image

    def __repr__(self):
        return self.location


class Comment(db.Model):
    """
    Comment Model

    Members:
        ID      - Comment unique identifier
        post    - Parent post that the comment belongs to
        user    - User that made the comment
        content - Content of the comment
    """
    __tablename__ = "comment"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, db.ForeignKey("post.id"))
    content = db.Column(db.String(10000))
    user = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, post, content, user):
        self.post = post
        self.content = content
        self.user = user

    def __repr__(self):
        return "{0}: {1}".format(self.post.name, self.content[:25])


class Photo(db.Model):
    """
    Photo Model

    A full-sized uploaded image

    Members:
        ID            - Photo unique identifier
        filename      - Location of the image
        scaled_photos - Children of the Photo which refers to a scaled version
                          of the image
    """
    __tablename__ = "photo"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    scaledphotos = db.relationship("ScaledPhoto")

    def __init__(self, filename, description=""):
        self.filename = filename
        self.description = description

    def __repr__(self):
        return self.filename


class ScaledPhoto(db.Model):
    """
    Scale Photo Model

    A reference to a full-sized image that can be used to scale an image to fit
    a specific ratio

    Members:
        ID      - Scaled Photo unique identifier
        photo   - Reference to a full-sized photo
        topoff  - Offset from the top of the image in pixels
        leftoff - Offset from the left of the image in pixels
        ratio   - The expected ratio of the image to be scaled
    """
    
    __tablename__ = "scaledphoto"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Integer, db.ForeignKey("photo.id"))
    topoff = db.Column(db.Integer)
    leftoff = db.Column(db.Integer)
    ratio = db.Column(db.String(10))

    def __init__(self, photo, topoff, leftoff, ratio):
        self.photo = photo
        self.topoff = topoff
        self.leftoff = leftoff
        self.ratio = ratio

    def __repr__(self):
        return "{0}:{1}".format(self.photo.filename, self.id)


Models = {
    "comments": Comment,
    "photos": Photo,
    "posts": Post,
    "roles": Role,
    "scaled": ScaledPhoto,
    "trips": Trip,
    "users": User,
}

ATR_DISP_ORD = {
    "comments": ["id", "user", "content"],
    "photos": ["id", "filename"],
    "posts": ["id", "title", "state", "post_date", "trip"],
    "roles": ["id", "name", "description"],
    "scaled": ["id", "photo", "leftoff", "topoff"],
    "trips": ["id", "location", "start_date", "end_date"],
    "users": ["id", "name", "email"],
}
