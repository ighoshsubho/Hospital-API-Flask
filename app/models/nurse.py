from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField
from app.models.hospital import HospitalShift

class Nurse(Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    shifts = ListField(ReferenceField(HospitalShift))

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'shifts': [shift.to_dict() for shift in self.shifts]
        }

class HospitalShift(Document):
    hospital = StringField(required=True)
    location = StringField(required=True)
    date = DateTimeField(required=True)
    start_time = StringField(required=True)
    end_time = StringField(required=True)
    price_per_hour = StringField(required=True)
    selected_nurse = ReferenceField(Nurse, null=True)

    def to_dict(self):
        return {
            'id': str(self.id),
            'hospital': self.hospital,
            'location': self.location,
            'date': self.date.strftime('%Y-%m-%d'),
            'start_time': self.start_time,
            'end_time': self.end_time,
            'price_per_hour': self.price_per_hour,
            'selected_nurse': self.selected_nurse.to_dict() if self.selected_nurse else None
        }
