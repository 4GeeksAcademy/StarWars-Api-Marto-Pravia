"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/api/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/api/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/api/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character no encontrdo"}), 404
    return jsonify(person.serialize()), 200

@app.route('/api/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/api/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/api/users/email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.serialize())

@app.route('/api/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1  
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

@app.route('/api/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  
    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

@app.route('/api/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1  
    new_favorite = Favorite(user_id=user_id, character_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

@app.route('/api/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1  
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorito no encontrado"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

@app.route('/api/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 1  
    favorite = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    if not favorite:
        return jsonify({"error": "favorito no encontrdo"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado"}), 200

@app.route('/api/planets', methods=['POST'])
def add_planet():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No hay info aqui"}), 400

    name = data.get('name')
    uid = data.get('uid')
    climate = data.get('climate')
    terrain = data.get('terrain')
    population = data.get('population')
    url = data.get('url')

    if not name or not uid:
        return jsonify({"error": "El nombre y el UID es obligatorio"}), 400

    new_planet = Planet(
        name=name,
        uid=uid,
        climate=climate,
        terrain=terrain,
        population=population,
        url=url
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201


@app.route('/api/characters', methods=['POST'])
def add_character():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No hay info aqui"}), 400

    name = data.get('name')
    uid = data.get('uid')
    gender = data.get('gender')
    birth_year = data.get('birth_year')
    height = data.get('height')
    url = data.get('url')

    if not name or not uid:
        return jsonify({"error": "El nombre y el UID es obligatorio"}), 400

    new_character = Character(
        name=name,
        uid=uid,
        gender=gender,
        birth_year=birth_year,
        height=height,
        url=url
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

@app.route('/api/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "no se encuentra palneta"}), 404

    db.session.delete(planet)
    db.session.commit()
    return jsonify({"message": f"Planet {planet.name} fue borrado"}), 200

@app.route('/api/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "Character no encontrado"}), 404

    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": f"Character {character.name} fue borrado"}), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "User already exists with this email"}), 400

    new_user = User(
        email=data['email'],
        password=data['password'],
        is_active=True  
    )

    
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
