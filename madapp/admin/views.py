from flask import render_template, url_for, Blueprint, abort, redirect, request
from flask_security import (Security, SQLAlchemyUserDatastore, UserMixin,
                            RoleMixin, login_required, current_user)
from madapp import db
from madapp.admin.db_handlers import DBHandlers
from madapp.admin.forms import AdminForms
from madapp.models import Models, ATR_DISP_ORD
import flask_login as login
import os
from pprint import pprint

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


def is_accessible():
    if not current_user.is_authenticated or not current_user.is_active:
        return False
    if current_user.has_role("sysadmin"):
        return True
    return False


@admin_bp.route("/")
def main():
    if not is_accessible():
        return redirect(url_for("security.login", next=request.url))
    return render_template("admin/index.html")


@admin_bp.route("/<admin_type>", methods=["GET", "POST"])
def admin_display(admin_type):
    if not is_accessible():
        return redirect(url_for("security.login", next=request.url))
    if admin_type.lower() not in Models.keys():
        abort(404)

    selected = request.form.getlist("selected")
    if len(selected) > 0:
        if request.form['btn'].lower() in ['delete']:
            for item in selected:
                Models[admin_type.lower()].query.filter_by(id=item).delete()
            db.session.commit()
        if request.form['btn'].lower() in ['modify']:
            return redirect(url_for("admin_bp.modify_entry",
                                    admin_type=admin_type,
                                    element_id=item))

    display_data = Models[admin_type.lower()].query.all()
    return render_template("admin/display.html",
                           admin_type=admin_type,
                           data=display_data,
                           attrs_order=ATR_DISP_ORD[admin_type])


@admin_bp.route("/<admin_type>/add", methods=["GET", "POST"])
def create_new(admin_type):
    form = AdminForms[admin_type.lower()]()
    form._path = admin_type
    if not is_accessible():
        return redirect(url_for("security.login", next=request.url))
    if form.validate_on_submit():
        print "VALIDATE ON SUBMIT"
        DBHandlers[admin_type.lower()](form)
        return redirect(url_for("admin_bp.admin_display", admin_type=admin_type))
    else:
        print "Not validated"
    enct = ""
    if admin_type.lower() in ["photos"]:
        enct = "multipart/form-data"
    return render_template("admin/add.html",
                           admin_form=form,
                           admin_type=admin_type,
                           enctype=enct)


@admin_bp.route("/<admin_type>/modify/<element_id>", methods=["GET", "POST"])
def element_modify(admin_type, element_id):
    if not is_accessible():
        return redirect(url_for("security.login", next=request.url))
    if request.method == "POST":
        pass
    return render_template("admin/modify".format(admin_type))


@admin_bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
