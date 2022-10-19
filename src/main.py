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
import json 

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
    return jsonify(usuario), 200


# Alta de un usuario
@app.route('/user', methods=['POST'])
def addUser():
    body = json.loads(request.data)

    queryNewUser = User.query.filter_by(email=body["email"]).first()
    
    if queryNewUser is None:
        new_user = User(name=body["name"], 
        lastname=body["lastname"], 
        username=body["username"], 
        email=body["email"], 
        password=body["password"])
        
        db.session.add(new_user)
        db.session.commit()
        
        response_body = {
            "msg": "Nuevo usuario creado" 
        }
        return jsonify(new_user.serialize()), 200
    
    response_body = {
        "msg": "Usuario ya creado" 
    }
    return jsonify(response_body), 400

# Modifica un usuario por id
@app.route('/user/<int:user_id>', methods=['PUT'])
def usersModif_porId(user_id):
    usuario = User.query.filter_by(id=user_id).first()
    body = json.loads(request.data)

    if usuario is None:
        response_body = {"msg": "No existe el usuario"}
        return jsonify(response_body), 400    

    if "email" in body:
        usuario.email = body["email"]
    if "name" in body:
        usuario.name = body["name"]
    if "lastname" in body:
        usuario.lastname = body["lastname"]
    if "username" in body:
        usuario.username = body["username"]
    
    db.session.commit()
    response_body = {"msg": "Usuario modificado"}
    return jsonify(response_body), 400


# Borra un usuario
@app.route('/user/<int:user_id>', methods=['DELETE'])
def deleteUser(user_id):
    userId = User.query.filter_by(id=user_id).first()
  
    if userId is None: 
        response_body = {"msg": "Usuario no encontrado"}
        return jsonify(response_body), 400

    db.session.delete(userId)
    db.session.commit()
    response_body = {"msg": "Usuario borrado"}
    return jsonify(response_body), 200


########################
#       Planetas       #
########################
# Muestra todos los planetas
@app.route('/planets', methods=['GET'])
def all_planets():
    planetas = Planets.query.all()
    results = list(map(lambda x: x.serialize(), planetas))
    return jsonify(results), 200

# Muestra planetas por id
@app.route('/planets/<int:planet_id>', methods=['GET'])
def planets_porId(planet_id):
    planeta = Planets.query.filter_by(id=planet_id).first()
    planet = planeta.serialize()
    return jsonify(planet), 200


# Alta de un planeta
@app.route('/planets', methods=['POST'])
def addPlanets():
    body = json.loads(request.data)

    queryNewPlanet = Planets.query.filter_by(name=body["name"]).first()
    
    if queryNewPlanet is None:
        new_planet = Planets(name=body["name"])
        
        db.session.add(new_planet)
        db.session.commit()
        
        response_body = {
            "msg": "Nuevo planeta creado" 
        }
        return jsonify(new_planet.serialize()), 200
    
    response_body = {
        "msg": "Planeta ya creado" 
    }
    return jsonify(response_body), 400

# Modifica un planeta por id
@app.route('/planets/<int:planets_id>', methods=['PUT'])
def planetsModif_porId(planets_id):
    planeta = Planets.query.filter_by(id=planets_id).first()
    body = json.loads(request.data)

    if planeta is None:
        response_body = {"msg": "No existe el planeta"}
        return jsonify(response_body), 400    

    if "name" in body:
        planeta.name = body["name"]
    db.session.commit()
    response_body = {"msg": "Planeta modificado"}
    return jsonify(response_body), 400

# Borra un Planeta
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def deletePlanet(planet_id):
    planetId = Planets.query.filter_by(id=planet_id).first()
  
    if planetId is None: 
        response_body = {"msg": "Planeta no encontrado"}
        return jsonify(response_body), 400

    db.session.delete(planetId)
    db.session.commit()
    response_body = {"msg": "Planeta borrado"}
    return jsonify(response_body), 200


########################
#       Personajes     #
########################
# Muestra todos los personajes
@app.route('/characters', methods=['GET'])
def all_characters():
    personaje = Characters.query.all()
    results = list(map(lambda x: x.serialize(), personaje))
    return jsonify(results), 200

# Muestra personajes por id
@app.route('/characters/<int:characters_id>', methods=['GET'])
def characters_porId(characters_id):
    personaje = Characters.query.filter_by(id=characters_id).first()
    char = personaje.serialize()
    return jsonify(char), 200


# Modifica un personaje por id
@app.route('/characters/<int:characters_id>', methods=['PUT'])
def charactersModif_porId(characters_id):
    personaje = Characters.query.filter_by(id=characters_id).first()
    body = json.loads(request.data)

    if personaje is None:
        response_body = {"msg": "No existe el personaje"}
        return jsonify(response_body), 400    

    if "name" in body:
        personaje.name = body["name"]
    if "lastName" in body:
        personaje.lastname = body["lastName"]
    db.session.commit()
    response_body = {"msg": "Personaje modificado"}
    return jsonify(response_body), 400

# Alta de un personaje
@app.route('/characters', methods=['POST'])
def add_Characters():
    body = json.loads(request.data)

    queryNewCharacter = Characters.query.filter_by(name=body["name"]).first()
    
    if queryNewCharacter is None:
        new_charc = Characters(name=body["name"], 
        lastName=body["lastName"])
        
        db.session.add(new_charc)
        db.session.commit()
        
        response_body = {
            "msg": "Nuevo personaje creado" 
        }
        return jsonify(new_charc.serialize()), 200
    
    response_body = {
        "msg": "Personaje ya creado" 
    }
    return jsonify(response_body), 400

# Borra un Personaje
@app.route('/characters/<int:character_id>', methods=['DELETE'])
def deletePersonaje(character_id):
    personajeId = Characters.query.filter_by(id=character_id).first()
  
    if personajeId is None: 
        response_body = {"msg": "Personaje no encontrado"}
        return jsonify(response_body), 400

    db.session.delete(personajeId)
    db.session.commit()
    response_body = {"msg": "Personaje borrado"}
    return jsonify(response_body), 200

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

# Borra la lista de los favoritos
@app.route('/favorite/<int:fav_id>', methods=['DELETE'])
def deleteFavorite(fav_id):
    favId = Favorites.query.filter_by(id=fav_id).first()
  
    if favId is None: 
        response_body = {"msg": "Favoritos no encontrado"}
        return jsonify(response_body), 400

    db.session.delete(favId)
    db.session.commit()
   
    response_body = {"msg": "Favorito borrado"}
    return jsonify(response_body), 200


# Borra un determinado planeta de la lista de los favoritos
@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def deleteFavoritePlanet(user_id, planet_id):
    
    # Controla que exista el usuario
    favUser = Favorites.query.filter_by(id_user=user_id).first()
    if favUser is None: 
        response_body = {"msg": "Usuario no encontrado"}
        return jsonify(response_body), 400

     # Controla que exista el planeta
    favId = Favorites.query.filter_by(id_planets=planet_id).first()
    if favId is None: 
        response_body = {"msg": "Planeta no encontrado"}
        return jsonify(response_body), 400

    #Borra el planeta segun el usuario
    favorito = Favorites.query.filter_by(id_user=user_id).filter_by(id_planets=planet_id).first()
#    print(favorito)

    db.session.delete(favorito)
    db.session.commit()
   
    response_body = {"msg": "Favorito borrado"}
    return jsonify(response_body), 200

# Borra un determinado personaje de la lista de los favoritos
@app.route('/favorite/character/<int:user_id>/<int:characters_id>', methods=['DELETE'])
def deleteFavoriteCharacter(user_id, characters_id):
    
    # Controla que exista el usuario
    favUser = Favorites.query.filter_by(id_user=user_id).first()
    if favUser is None: 
        response_body = {"msg": "Usuario no encontrado"}
        return jsonify(response_body), 400

     # Controla que exista el personaje
    favId = Favorites.query.filter_by(id_characters=characters_id).first()
    if favId is None: 
        response_body = {"msg": "Personaje no encontrado"}
        return jsonify(response_body), 400

    #Borra el planeta segun el usuario
    favorito = Favorites.query.filter_by(id_user=user_id).filter_by(id_characters=characters_id).first()

    db.session.delete(favorito)
    db.session.commit()
    response_body = {"msg": "Personaje favorito borrado"}
    return jsonify(response_body), 200

# Le agrega un nuevo planeta favorito a un usuario
@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def add_FavoritePlanet(user_id, planet_id):

    # Controla que exista el usuario
    favUser = Favorites.query.filter_by(id_user=user_id).first()
    if favUser:
        # Controla que existan planetas
        favId = Favorites.query.filter_by(id_planets=planet_id).first()
        if favId: 
            # Ya existe ese planeta para ese usuario
            response_body = {"msg": "Planeta existente para ese usuario"}
            return jsonify(response_body), 400
        else: 
            #Si no tiene ese planeta, lo agrega
            new_Favorito = Favorites(id_user=user_id, id_planets=planet_id)
        
            db.session.add(new_Favorito)
            db.session.commit()
            
            response_body = {"msg": "Favorito creado" }
            return jsonify(response_body), 200
    else:
        # Ya existe ese planeta para ese usuario
        response_body = {"msg": "No existe el usuario"}
        return jsonify(response_body), 400

# Le agrega un nuevo personaje favorito a un usuario
@app.route('/favorite/character/<int:user_id>/<int:char_id>', methods=['POST'])
def add_FavoriteChar(user_id, char_id):

    # Controla que exista el usuario
    favUser = Favorites.query.filter_by(id_user=user_id).first()
    if favUser:
        # Controla que exista el personaje
        favId = Favorites.query.filter_by(id_characters=char_id).first()
        if favId: 
            # Ya existe ese personaje para ese usuario
            response_body = {"msg": "Este personaje ya es favorito para ese usuario"}
            return jsonify(response_body), 400
        else: 
            #Si no tiene ese personaje, lo agrega
            new_Favorito = Favorites(id_user=user_id, id_characters=char_id)
        
            db.session.add(new_Favorito)
            db.session.commit()
            
            response_body = {"msg": "Favorito creado" }
            return jsonify(response_body), 200
    else:
        # Ya existe ese personaje para ese usuario
        response_body = {"msg": "No existe el usuario"}
        return jsonify(response_body), 400


# Agrega un nuevo favorito
@app.route('/favorite', methods=['POST'])
def add_Favorites():
    body = json.loads(request.data)

    # Chequeo de ids de usuarios, planetas y personajes. 
    existeUser = User.query.filter_by(id=body["id_user"]).first()
    existePlanet = Planets.query.filter_by(id=body["id_planets"]).first()
    existePers = Characters.query.filter_by(id=body["id_characters"]).first()

     # Si se ingresa usuario, planeta y personaje.
    if existeUser: 
        if existePlanet:
            if existePers:
                # Chequea que exista ese usuario en la tabla de favoritos
                userinFav = Favorites.query.filter_by(id_user=body["id_user"]).first()
                # Si no existe crea el nuevo favorito con planeta y personaje
                if userinFav is None:
                    new_Favorito = Favorites(id_user=body["id_user"], 
                    id_planets=body["id_planets"], id_characters=body["id_characters"])
                
                    db.session.add(new_Favorito)
                    db.session.commit()
                    
                    response_body = {"msg": "Favorito creado"}
                    return jsonify(response_body), 200
                else: 
                    #Si existe el usuario, chequea que no tenga ese planeta
                    planetFav = Favorites.query.filter_by(id_planets=body["id_planets"]).first()
                    #Si no encuentra ese planeta, chequea que no tenga ningun personaje
                    if planetFav is None:
                        persFav = Favorites.query.filter_by(id_characters=body["id_characters"]).first()
                        # Si no encuentra ningun personaje, crea todo
                        if persFav is None: 
                            new_Favorito = Favorites(id_user=body["id_user"], 
                            id_planets=body["id_planets"], id_characters=body["id_characters"])
                
                            db.session.add(new_Favorito)
                            db.session.commit()
                    
                            response_body = {"msg": "Favorito creado"}
                            return jsonify(response_body), 200
                        else:
                            #Modifica el planeta
                            if "id_planets" in body:
                                planetFav.id_planets = body["id_planets"]
                            db.session.commit()
                            response_body = {"msg": "Planeta modificado"}
            else: 
                response_body = {"msg": "Personaje no creado"}
                return jsonify(response_body), 400
        else: 
            response_body = {"msg": "Planeta no creado"}
            return jsonify(response_body), 400
    else: 
        response_body = {"msg": "Usuario no creado"}
        return jsonify(response_body), 400
    #print(body["id_characters"])
   
    # Si se ingresa usuario y planeta solamente.
    if existeUser:
        if existePlanet:
            new_Favorito = Favorites(id_user=body["id_user"], 
            id_planets=body["id_planets"])
        
            db.session.add(new_Favorito)
            db.session.commit()
            
            response_body = {
                "msg": "Favorito creado" 
            }
            return jsonify(response_body), 200
        else: 
            response_body = {"msg": "Planeta no creado"}
            return jsonify(response_body), 200
    else: 
        response_body = {"msg": "Usuario no creado"}
        return jsonify(response_body), 200
        
    # Si se ingresa usuario y personaje solamente.
    if existeUser:
        if existePers:
            new_Favorito = Favorites(id_user=body["id_user"], 
            id_characters=body["id_characters"])
        
            db.session.add(new_Favorito)
            db.session.commit()
            
            response_body = {
                "msg": "Favorito creado" 
            }
            return jsonify(response_body), 200
        else:
            response_body = {"msg": "Personaje no creado"}
            return jsonify(response_body), 200
    else: 
        response_body = {"msg": "Usuario no creado"}
        return jsonify(response_body), 200
   
    response_body = {
        "msg": "Error al agregar favoritos" 
    }
    return jsonify(response_body), 400


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)