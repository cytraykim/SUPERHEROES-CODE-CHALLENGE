from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    powers = db.relationship('HeroPower', back_populates='hero')
    

class Power(db.Model):
    __tablename__ = "powers"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique = True)
    description = db.Column(db.String)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    heroes = db.relationship('HeroPower', back_populates='power')
    
    def _repr_(self):
        return f'(id={self.id}, name={self.name} description={self.description})'
    
    @validates('description')
    def checks_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be longer than 20 chars")
        else:
            return description

class HeroPower(db.Model):
    __tablename__ = "hero_powers"
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    
    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')
    
    
    
    @validates('strength')
    def checks_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be a value either 'Strong', 'Weak' or 'Average'")
        else:
            return strength
