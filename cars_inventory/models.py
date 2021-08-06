from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid


from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import LoginManager, login_manager, UserMixin

from flask_marshmallow import Marshmallow


db = SQLAlchemy()

login_manager = LoginManager()

ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False, unique=True)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Cars', backref = 'owner', lazy = True)



    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

class Cars(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale=2))
    travel_range = db.Column(db.String(150))
    passengers = db.Column(db.String(50))
    cost_of_prod = db.Column(db.Numeric(precision=10, scale=2))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, travel_range, passengers, cost_of_prod, user_token, id = '' ):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.travel_range = travel_range
        self.passengers = passengers
        self.cost_of_prod = cost_of_prod
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())

    
class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'travel_range', 'passengers', 'cost_of_prod' ]

car_schema = CarSchema()
cars_schema = CarSchema(many=True)
