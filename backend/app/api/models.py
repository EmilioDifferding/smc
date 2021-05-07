"""
models.py
- Data classes for the surveyapi application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from werkzeug.security import generate_password_hash, check_password_hash

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    aliases = db.relationship('Alias', backref='device', lazy='dynamic')
    unic_id = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    measurements = db.relationship('Measurement', backref='device', lazy='dynamic')

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            unic_id=self.unic_id,
            place=self.place.to_dict(),
            aliases=[alias.to_dict() for alias in self.aliases]
        )

class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    symbol = db.Column(db.String(10))
    aliases = db.relationship('Alias', backref='unit', lazy='dynamic')

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            symbol=self.symbol
        )

class Alias(db.Model):
    __tablename__ = 'aliases'
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    name = db.Column(db.String(20))
    values = db.relationship('Value', backref='alias', lazy='dynamic')
    max_limit = db.Column(db.Float, nullable=True)
    min_limit = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            max_limit=self.max_limit,
            min_limit=self.min_limit,
            device_id=self.device_id,
            device_name=self.device.name,
            unit=self.unit.to_dict(),
            # unit_id=self.unit_id,
            # unit_name=self.unit.name,
            # unit_symbol=self.unit.symbol,
        )

class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    values = db.relationship('Value', backref='measurement',lazy='dynamic')
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    

    def to_dict(self):
        return dict(
            id=self.id,
            timestamp=self.timestamp.strftime('%d/%m/%Y %H:%M:%S'),          
            device_id=self.device_id,
            values=[value.to_dict() for value in self.values]
        )

class Value (db.Model): 
    __tablename__ = 'values'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    measurement_id = db.Column(db.Integer, db.ForeignKey('measurements.id'))
    alias_id = db.Column(db.Integer, db.ForeignKey('aliases.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            value=self.value,
            alias=self.alias.name,
            measurement_id=self.measurement_id,
        )

class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, nullable=False)
    devices = db.relationship('Device', backref='place', lazy='dynamic')

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
        )

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, nullable=False)
    email= db.Column(db.String(100), index=True, nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    telegram_id = db.Column(db.Integer)



    def __init__(self,name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        
    
    @classmethod 
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None
        
        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None
        
        return user
    
    def to_dict(self):
        return dict(id=self.id, name=self.name, email=self.email)