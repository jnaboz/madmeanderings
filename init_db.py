from madapp import db, user_datastore, security
from madapp.models import User, Role
from flask_security.utils import encrypt_password

db.create_all()

author_role = Role(name="author", description="")
admin_role = Role(name="sysadmin", description="")
db.session.add(admin_role)
db.session.add(author_role)
db.session.commit()

db.session.add(User(name="admin",
                    email="admin",
                    password="a",
                    roles=[admin_role, author_role]))
db.session.commit()
