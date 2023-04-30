from datetime import datetime
from app import db

class Hospital(db.Document):
    name = db.StringField(required=True, max_length=100)
    location = db.StringField(required=True)
    shifts = db.ListField(db.EmbeddedDocumentField('Shift'))

class Shift(db.EmbeddedDocument):
    date = db.DateTimeField(required=True, default=datetime.now())
    start_time = db.StringField(required=True)
    end_time = db.StringField(required=True)
    price_per_hour = db.FloatField(required=True)

    def to_dict(self):
        return {
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'price_per_hour': self.price_per_hour
        }
