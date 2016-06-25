from madapp import IMAGE_SET
from madapp.models import Models
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
import re
from wtforms import (StringField, PasswordField, IntegerField, DateField,
                     BooleanField, SelectField, SelectMultipleField, TextAreaField)
from wtforms.validators import (Required, Optional, Length, EqualTo, Email, regexp)


class DynamicSelectMultipleField(SelectMultipleField):
    """ Allows to dynamically populate a Select field, such as a DB source"""
    def pre_validate(self, form):
        for v, _ in self.choices:
            if True:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class DynamicSelectField(SelectField):
    """ Allows to dynamically populate a Select field, such as a DB source"""
    def pre_validate(self, form):
        for v, _ in self.choices:
            if True:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class PostForm(Form):
    trip = DynamicSelectField("Trip", validators=[Required()])
    title = StringField("Title", validators=[Required()])
    content = TextAreaField("Content", validators=[Required()])

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.trip.choices = [(x.id, x.location) for x in Models["trips"].query.all()]


class RoleForm(Form):
    name = StringField("Role Name", validators=[Required(), Length(min=1, max=50)])
    description = StringField("Description", validators=[Optional(), Length(max=100)])


class TripForm(Form):
    location = StringField("Trip Location", validators=[Required(), Length(min=1, max=255)])
    start_date = DateField("Start Date", validators=[Required()])
    end_date = DateField("End Date", validators=[Required()])
    cover = DynamicSelectField("Cover Image", validators=[Required()])

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.cover.choices = [(x.id, x.filename) for x in Models["photos"].query.all()]


class UploadForm(Form):
    image = FileField("Image File", validators=[FileRequired(), FileAllowed(IMAGE_SET, "Images Only!")])
    description = StringField("Image Description", validators=[Optional(), Length(max=255)])


class UserForm(Form):
    name = StringField("Name", validators=[Required(), Length(min=1, max=50)])
    password = PasswordField("Password", validators=[Required(), Length(min=8, max=100), EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Repeat password")
    email = StringField("Email address", validators=[Optional(), Email(), Length(max=100)])
    roles = DynamicSelectMultipleField("Roles", validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.roles.choices = [(x.id, x.name) for x in Models["roles"].query.all()]


AdminForms = {
    "photos": UploadForm,
    "posts": PostForm,
    "roles": RoleForm,
    "trips": TripForm,
    "users": UserForm,
}
