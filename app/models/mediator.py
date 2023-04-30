from app import db

class Mediator(db.Document):
    name = db.StringField(required=True, max_length=100)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
