from madapp import db
from madapp.models import User, Role
from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import encrypt_password

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

db.create_all()

author_role = Role(name="author")
admin_role = Role(name="administrator")
db.session.add(admin_role)
db.session.add(author_role)
db.session.commit()

#user_datastore.create_user(
#        name="admin",
#        email="admin",
#        password=encrypt_password("a"),
#        roles=[admin_role, author_role])
#
#db.session.commit()
