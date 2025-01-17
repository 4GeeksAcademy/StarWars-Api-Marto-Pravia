from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorite', backref='user')

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(100))
    terrain = db.Column(db.String(100))
    population = db.Column(db.String(100))
    url = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "url": self.url,
        }
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(100), unique=True, nullable=False)  
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(30))
    birth_year = db.Column(db.String(30))
    height = db.Column(db.String(30))
    url = db.Column(db.String(200)) 

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "url": self.url,
        }
            
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)

    def __repr__(self):
        return f'<Favorite user_id={self.user_id} planet_id={self.planet_id} character_id={self.character_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
        }