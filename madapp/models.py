from madapp import db
from sqlalchemy_utils.types import ChoiceType
from flask_security import (UserMixin, RoleMixin)


POST_STATES = {
    "DR": "Draft",
    "PU": "Published",
}

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id"))
)


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    __bind_key__ = "blogdb"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50), unique=True)
    description = db.Column(db.Unicode(100))

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
    name = db.Column(db.Unicode(50))
    email = db.Column(db.Unicode(100), unique=True)
    password = db.Column(db.Unicode(100))
    active = db.Column(db.Boolean())
    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref("users", lazy="dynamic"))

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
    title = db.Column(db.Unicode(100))
    state = db.Column(ChoiceType(POST_STATES))
    tags = db.Column(db.String(100))
    trip = db.Column(db.Integer, db.ForeignKey("trip.id"))
    comments = db.relationship("Comment")
    content = db.Column(db.Unicode())


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
    posts = db.relationship("Post")
    location = db.Column(db.Unicode(255), unique=True)
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    cover_image = db.Column(db.Integer, db.ForeignKey("scaledphoto.id"))


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
    content = db.Column(db.Unicode(1000))
    user = db.Column(db.Integer, db.ForeignKey("user.id"))


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
    scaledphotos = db.relationship("ScaledPhoto")


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
