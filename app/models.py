from . import db

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(800))
    no_rooms = db.Column(db.Integer)
    no_bathrooms = db.Column(db.Integer)
    price = db.Column(db.Integer)
    property_type = db.Column(db.String(30))
    location = db.Column(db.String(150))
    photo = db.Column(db.String(250))

    def __init__(self, title, description, no_rooms, no_bathrooms, price, property_type, location, photo):
        self.title = title
        self.description = description
        self.no_rooms = no_rooms
        self.no_bathrooms = no_bathrooms
        self.price = price
        self.property_type = property_type
        self.location = location
        self.photo = photo


    def __repr__(self):
        return f'<Property {self.id}>'