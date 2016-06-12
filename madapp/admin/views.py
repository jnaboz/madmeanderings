from madapp import fadmin, db
from madapp.models import Comment, User, Post, Trip, Photo, ScaledPhoto, Role
from flask import render_template, url_for, Blueprint, abort, redirect
#from flask_admin import BaseView, expose
#from flask_admin.contrib.fileadmin import FileAdmin
#from flask_admin.contrib.sqla import ModelView
#from flask_admin.form import SecureForm
import flask_login as login
from flask_security import (Security, SQLAlchemyUserDatastore, UserMixin,
                            RoleMixin, login_required, current_user)
import os

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route("/")
def main():
    if(not current_user.is_authenticated or
       not current_user.is_active or
       not current_user.has_role("sysadmin")):
        return redirect(url_for("security.login", next=request.url))
    return render_template("admin/index.html")


#class AdminModelView(ModelView):
#    #form_base_class = SecureForm
#
#    #@expose("/")
#    #def main(self):
#    #    return self.render("admin/main.html")
#
#    #@expose("/post")
#    #def submit_new_post(self):
#    #    return self.render("admin/new_post.html")
#
#    def is_accessible(self):
#        print "CURRENT USER: {0}".format(current_user.is_authenticated)
#        if not current_user.is_active or not current_user.is_authenticated:
#            return False
#        if current_user.has_role("sysadmin"):
#            return True
#        return False
#
#    def _handle_view(self, name, **kwargs):
#        print "handle view"
#        if not self.is_accessible():
#            if current_user.is_authenticated:
#                abort(403)
#            else:
#                return redirect(url_for("security.login", next=request.url))
#
#
#class AdminFileView(FileAdmin):
#    def is_accessible(self):
#        print "CURRENT USER: {0}".format(current_user.is_authenticated)
#        if not current_user.is_active or not current_user.is_authenticated:
#            return False
#        if current_user.has_role("sysadmin"):
#            return True
#        return False
#
#    def _handle_view(self, name, **kwargs):
#        print "handle view"
#        if not self.is_accessible():
#            if current_user.is_authenticated:
#                abort(403)
#            else:
#                return redirect(url_for("security.login", next=request.url))

#fadmin.add_view(AdminModelView(Role, db.session))
#fadmin.add_view(AdminModelView(User, db.session))
#fadmin.add_view(AdminModelView(Trip, db.session))
#fadmin.add_view(AdminModelView(Post, db.session))
#fadmin.add_view(AdminModelView(Photo, db.session))
#fadmin.add_view(AdminModelView(ScaledPhoto, db.session))
#path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#path = os.path.join(path, "static/uploads")
#fadmin.add_view(AdminFileView(path, '/static/uploads/', name="Upload Images"))
