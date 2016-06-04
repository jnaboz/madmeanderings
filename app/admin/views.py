from flask import render_template, Blueprint, url_for

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route("/")
def main():
    return render_template("admin/main.html")
