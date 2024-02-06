#!/usr/bin/env python3

# app.py
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
    return jsonify(hero_data)

# GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [{"id": p.id, "name": p.name, "description": p.description} for p in hero.powers]
        }
        return jsonify(hero_data)
    else:
        return make_response(jsonify({"error": "Hero not found"}), 404)

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(power_data)

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        return jsonify(power_data)
    else:
        return make_response(jsonify({"error": "Power not found"}), 404)

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.get_json()
        description = data.get('description')

        if description and len(description) >= 20:
            power.description = description
            db.session.commit()

            return jsonify({
                "id": power.id,
                "name": power.name,
                "description": power.description
            })
        else:
            return make_response(jsonify({"errors": ["Validation error: Description must be at least 20 characters long"]}), 400)
    else:
        return make_response(jsonify({"error": "Power not found"}), 404)

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero and power and strength in ['Strong', 'Weak', 'Average']:
        hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
        db.session.add(hero_power)
        db.session.commit()

        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [{"id": p.id, "name": p.name, "description": p.description} for p in hero.powers]
        }

        return jsonify(hero_data)
    else:
        return make_response(jsonify({"errors": ["Validation error: Invalid hero or power ID or strength"]}), 400)

if __name__ == '__main__':
    app.run(port=5555)

