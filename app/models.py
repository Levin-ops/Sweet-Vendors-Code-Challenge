from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship, validates
from datetime import datetime

db = SQLAlchemy()

class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow)
    # Relationships
    vendor_sweets = db.relationship('Vendor_Sweets', back_populates='vendor')
    sweets = db.relationship('Sweet', secondary='vendor_sweets', back_populates='vendors')

    def __repr__(self):
        return f'<vendor {self.name}>'


class Vendor_Sweets(db.Model):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.String(255), nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow) 
    # relationships
    sweet = db.relationship('Sweet', back_populates='vendor_sweets')
    vendor = db.relationship('Vendor', back_populates='vendor_sweets')

    def __repr__(self):
        return f'<price {self.price}, vendor_id {self.vendor_id}, sweet_id {self.sweet_id}'
    

    @validates('price')
    def validates_price(self, key, price):
        if not price:
            raise ValueError("Price cannot be blank")

        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be a negative number")

        return price
    

class Sweet(db.Model):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow)
    # relationships
    vendor_sweets = db.relationship('Vendor_Sweets', back_populates='sweet')
    vendors = db.relationship('Vendor', secondary='vendor_sweets', back_populates='sweets')

