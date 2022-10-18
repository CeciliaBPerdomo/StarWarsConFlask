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
from models import db, User, Planets, Characters, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

########################
#       Usuarios       #
########################

# Muestra todos los usuarios
@app.route('/user', methods=['GET'])
def handle_hello():
    user = User.query.all()
    results = list(map(lambda x: x.serialize(), user))
    print (results)
    return jsonify(results), 200

# Busca por id de usuario
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    userId = User.query.filter_by(id=user_id).first()
    usuario = userId.serialize()
    print(usuario)
    return jsonify(usuario), 200

########################
#       Planetas       #
########################
# Muestra todos los planetas
@app.route('/planets', methods=['GET'])
def all_planets():
    planetas = Planets.query.all()
    results = list(map(lambda x: x.serialize(), planetas))
    print (results)
    return jsonify(results), 200

# Muestra planetas por id
@app.route('/planets/<int:planet_id>', methods=['GET'])
def planets_porId(planet_id):
    planeta = Planets.query.filter_by(id=planet_id).first()
    planet = planeta.serialize()
    print(planet)
    return jsonify(planet), 200

########################
#       Personajes     #
########################
# Muestra todos los personajes
@app.route('/characters', methods=['GET'])
def all_characters():
    personaje = Characters.query.all()
    results = list(map(lambda x: x.serialize(), personaje))
    print (results)
    return jsonify(results), 200

# Muestra personajes por id
@app.route('/characters/<int:characters_id>', methods=['GET'])
def characters_porId(characters_id):
    personaje = Characters.query.filter_by(id=characters_id).first()
    char = personaje.serialize()
    print(char)
    return jsonify(char), 200


########################
#       Favoritos      #
########################
# Muestra todos los favoritos de todas las personas
@app.route('/favorits', methods=['GET'])
def favoritos():
    favoritos = Favorites.query.all()
    results = list(map(lambda x: x.serialize(), favoritos))
    print (results)
    return jsonify(results), 200

# Muestra favorito por id 
@app.route('/favorits/<int:favorits_id>', methods=['GET'])
def favorits_porId(favorits_id):
    favorito = Favorites.query.filter_by(id=favorits_id).first()
    favorite = favorito.serialize()
    print(favorite)
    return jsonify(favorite), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)