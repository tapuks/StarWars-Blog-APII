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
from models import db, User, Planets, People
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

# @app.route('/user', methods=['GET'])
# def handle_hello():
#     # users = User.query.all()
#     # print(users)
#     # users=[] 
#     # for user in users:
#     #     array.append(user.serialize())
#     # print(array)
#     # return jsonify({"users":array})
#     return jsonify({"users": users}),200

@app.route('/people', methods=['GET'])
def show_people():
    people = People.query.all()
    people_all = []
    for person in people:
        people_all.append( person.serialize())
    return jsonify({"people" : people_all}),200

@app.route('/people/<int:people_id>', methods=['GET'])
def show_one_people(people_id):
    person = People.query.filter_by(id = people_id).first()
    return jsonify(person.serialize()),200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_one_people(people_id):
    user = People.query.get(people_id)
    db.session.delete(user)
    db.session.commit()
    # show all
    people = People.query.all()
    people_all = []
    for person in people:
        people_all.append( person.serialize())
    return jsonify({"people" : people_all}),200

   
@app.route('/planets', methods=['GET'])
def show_all_planets():
    planets = Planets.query.all()
    planets_all = []
    for planet in planets:
        planets_all.append(planet.serialize())
    return jsonify({"planets":planets_all}),200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def show_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()
    serialize=planet.serialize()
    return jsonify(serialize),200

@app.route('/login', methods=['POST'])
def handle_login():
    print("@@@")
    json = request.get_json()

    # si no nos manda un json 
    if json is None:
        raise APIException("You should send json body")
    if "email" not in json or "password" not in json:
        raise APIException("Email and password are required")

    email = json["email"]
    password = json["password"]

    # Pregunta a la base de datos si tenemos un user con ese email y contraseña
    user = User.get_with_login_credentials(email, password)
    # print(user.serialize())
    if user is None:
        return "error", 306
        # raise APIException("User not found")

    token = "222edse2¡rwter7545teji9o"
    user.assign_token(token)
    print(user.serialize())
    #  devolvemos un usuario al frond
    return jsonify({"user": user.serialize(), "token": token}), 200

@app.route('/profile', methods=['POST'])
def handle_profile():
    json = request.get_json()
    token = json[token]
    user = User.get_with_token(token)
    if user is None: 
        raise APIException("Invalid token")
    return jsonify(user.serialize()), 200



# @app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
# def add_favourite_planet(planet_id):
#     body = request.get_json()
#     # print(body)
#     # print(planet_id)
#     favorites.append(body)
#     return jsonify({"favorites":favorites}),200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
