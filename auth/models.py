from typing import Optional
from flask import current_app
import sqlalchemy
import sqlalchemy.orm as orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, current_app.login_database.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(127), index=True, unique=True)
    email: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(127), index=True, unique=True)
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sqlalchemy.String(256))

    def set_password_hash(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, hash: str):
        return check_password_hash(self.password_hash, hash)

    def __repr__(self):
        return '<User %r>' % self.username

@current_app.login.user_loader
def load_user(id):
    return current_app.login_database.session.get(User, int(id))