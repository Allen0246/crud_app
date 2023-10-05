from .. import db
from flask_login import UserMixin

class User(db.Model , UserMixin):
    __tablename__ = 'felhasznalok'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(512))

    def __init__(self, username,password):
        self.username = username
        self.password = password

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_username_and_password(self, username, password):
        self.username = username
        self.password = password


db.create_all()
db.session.commit()
