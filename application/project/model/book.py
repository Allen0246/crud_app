from .. import db


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    szerzo = db.Column(db.String(100), nullable=False, unique=True)
    cim = db.Column(db.String(100), nullable=False, unique = True)

    def __init__(self, szerzo, cim):
        self.szerzo = szerzo
        self.cim = cim

    def set_author(self, szerzo):
        self.szerzo = szerzo

    def set_tittle(self, cim):
        self.cim = cim

db.create_all()
db.session.commit()