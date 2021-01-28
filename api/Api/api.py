from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

# IA imports
import pickle
import nltk as distance
import Pycluster as PC
import numpy
import pandas as pd
import csv
import time
import matplotlib.pyplot as plt
from unicodedata import normalize

import json
from json import JSONEncoder

app = Flask(__name__)


app.config["SECRET_KEY"] = "FuckTheRandomness"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://douglas:douglas98@localhost/tfgTest"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Models
# Table Users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    userName = db.Column(db.String(20))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


# Table testResidents
class TestR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    musicGender = db.Column(db.String(25))
    sport = db.Column(db.String(25))
    hobbie = db.Column(db.String(25))
    movieSeries = db.Column(db.String(10))
    filmGender = db.Column(db.String(25))
    tabaco = db.Column(db.Integer)
    alcohol = db.Column(db.Integer)
    party = db.Column(db.Integer)
    ordenConvivencia = db.Column(db.Integer)
    ordenPersonal = db.Column(db.Integer)
    personalidad = db.Column(db.String(10))  # Introver - Extro


# Table Residentes
class Residents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50))
    name = db.Column(db.String(30))
    lastName = db.Column(db.String(50))
    sharedRoom = db.Column(db.Boolean)


# Table Habitaciones


class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20))


# Table emparejamientos


class Matches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    room_id = db.Column(db.Integer)


# Api resources
# Token verification
# Ningun usuario podra acceder a los endpoints sin un token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

#EndPoints Crear usuario, residente y upgrade to admin
# Create new user
@app.route("/api/user", methods=["POST"])
# @token_required
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"], method="sha256")

    new_user = User(
        public_id=str(uuid.uuid4()),
        userName=data["userName"],
        password=hashed_password,
        admin=False,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "New user created!"})


# Create residente ( public_id = user.public_id, name, lastName, sharedRoom (True or false))
# json { "name": "name", "lastName": "lastname", "sharedRoom": "1/0"}
@app.route("/api/residente/<public_id>", methods=["POST"])
@token_required
def create_resident(current_user, public_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"})

    data = request.get_json()
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "Dude, no user found ! :("}), 404

    new_resident = Residents(
        public_id=public_id,
        name=data["name"],
        lastName=data["lastName"],
        sharedRoom=data["sharedRoom"],
    )

    db.session.add(new_resident)
    db.session.commit()

    return jsonify({"message": "New resident created!"}), 200


# Promover usuario a admin , solo un admin puede hacer eso
@app.route("/api/user/<public_id>", methods=["PUT"])
@token_required
def promote_user(current_user, public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "Dude, no user found ! :("})

    user.admin = True
    db.session.commit()
    return jsonify({"message": "user has been promoted!"})

# borrar un usuario, solo un admin podra
@app.route("/api/user/<public_id>", methods=["DELETE"])
@token_required
def delete_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "No user found!"})

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "The user has been deleted!"})




# EndPoints
# Get todos los usuarios
@app.route("/api/user", methods=["GET"])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data["user_id"] = user.id
        user_data["public_id"] = user.public_id
        user_data["userName"] = user.userName
        user_data["password "] = user.password
        user_data["admin"] = user.admin
        output.append(user_data)

    return jsonify({"users": output})


# Get all residentes
@app.route("/api/residents", methods=["GET"])
@token_required
def get_all_residents(current_user):

    if not current_user.admin:
        return jsonify({"message": "Cannot performs that funtion!"})

    residents = Residents.query.all()

    output = []

    for resident in residents:

        resident_data = {}
        resident_data["resident_Id"] = resident.id
        resident_data["public_Id"] = resident.public_id
        resident_data["name"] = resident.name
        resident_data["lastName"] = resident.lastName
        resident_data["sharedRoom"] = resident.sharedRoom
        output.append(resident_data)

    return jsonify({"residents": output})


# Get one resident info from resident by public id
@app.route("/api/resident/<public_id>", methods=["GET"])
@token_required
def get_resident(current_user, public_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot performs that funtion!"})

    resident = Residents.query.filter_by(public_id=public_id).first()
    if not resident:
        return jsonify({"message": "Dude, no resident found ! :("}), 404

    resident_data = {}
    resident_data["name"] = resident.name
    resident_data["lastName"] = resident.lastName
    resident_data["sharedRoom"] = resident.sharedRoom
    return jsonify({"resident": resident_data})


# get user/public_id usuario especifico
@app.route("/api/user/<public_id>", methods=["GET"])
@token_required
def get_one_user(current_user, public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "Dude, no user found ! :("})

    user_data = {}
    user_data["public_id"] = user.public_id
    user_data["userName"] = user.userName
    user_data["password "] = user.password
    user_data["admin"] = user.admin
    return jsonify({"user": user_data})




# Login , comprueba credenciales, genera token el cual se necesita para acceder a los endpoints
@app.route("/api/login")
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response("Falta Data", 401)

    user = User.query.filter_by(userName=auth.username).first()

    if not user:
        return make_response("Could not verify", 401)

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=45),
            },
            app.config["SECRET_KEY"],
        )

        return jsonify({"token": token.decode("UTF-8"), "admin": user.admin})

    return make_response("Could not verify", 401)


# ver perfil
@app.route("/api/perfil", methods=["GET"])
@token_required
def ver_perfil(current_user):

    # Object residente
    resident = Residents.query.filter_by(public_id=current_user.public_id).first()
    # Room, se tendra que ir a room buscar el id del usuario

    resident_data = {}
    resident_data["name"] = resident.name
    resident_data["lastName"] = resident.lastName
    resident_data["sharedRoom"] = resident.sharedRoom
    return jsonify({"resident": resident_data})

# get your personal result with your token xd
@app.route("/api/result", methods=["GET"])
@token_required
def get_result(current_user):

    resident = Residents.query.filter_by(public_id=current_user.public_id).first()

    if not resident:
        return jsonify({"message": "Dude, no resident found"}), 404

    matchR = Matches.query.filter_by(user_id=resident.public_id).first()
    if not matchR:
        return jsonify({"message": " Not result in match :("}), 404

    matchAll = Matches.query.filter_by(room_id=matchR.room_id).all()

    output = []

    for match in matchAll:
        match_data = {}
        resident = Residents.query.filter_by(public_id=match.user_id).first()
        if resident.public_id != current_user.public_id:
            match_data["room_id"] = match.room_id
            match_data["nameR"] = resident.name
            match_data["lastNameR"] = resident.lastName
            output.append(match_data)

    return jsonify({"matches": output})

# EndPoint test
# Hacer test, crea el test en base al currente user osea que el usuario que llame al endpoint de test guardara eso
@app.route("/api/test", methods=["POST"])
@token_required
def create_test(current_user):

    data = request.get_json()

    new_test = TestR(
        public_id=current_user.public_id,
        gender=data["gender"],
        age=data["age"],
        musicGender=data["musicGender"],
        sport=data["sport"],
        hobbie=data["hobbie"],
        movieSeries=data["movieSeries"],
        filmGender=data["filmGender"],
        tabaco=data["tabaco"],
        alcohol=data["alcohol"],
        party=data["party"],
        ordenConvivencia=data["ordenConvivencia"],
        ordenPersonal=data["ordenPersonal"],
        personalidad=data["personalidad"],
    )
    db.session.add(new_test)
    db.session.commit()

    return jsonify({"message": "Test created!!!"})




# obtener un test de usuario especifico
@app.route("/api/test/<public_id>", methods=["GET"])
@token_required
def get_one_test(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": "Dude, no user found ! :("})

    test = TestR.query.filter_by(user_id=user.public_id).first()

    if not test:
        return jsonify({"message": "Dude, no test available ! :("})

    test_data = {}

    test_data["gender"] = test.gender
    test_data["age"] = test.age
    test_data["musicGender"] = test.musicGender
    test_data["sport"] = test.sport
    test_data["hobbie"] = test.hobbie
    test_data["movieSeries"] = test.movieSeries
    test_data["filmGender"] = test.filmGender
    test_data["tabaco"] = test.tabaco
    test_data["alcohol"] = test.alcohol
    test_data["party"] = test.party
    test_data["ordenConvivencia"] = test.ordenConvivencia
    test_data["ordenPersonal"] = test.ordenPersonal
    test_data["personalidad"] = test.personalidad
    return jsonify({"test": test_data})

# get all test avaible
@app.route("/api/allTest", methods=["GET"])
@token_required
def get_all_test(current_user):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"})

    tests = TestR.query.all()

    output = []

    for test in tests:
        test_data = {}
        resident = Residents.query.filter_by(public_id=test.public_id).first()
        test_data["resident_id"] = resident.id
        test_data["gender"] = test.gender
        test_data["age"] = test.age
        test_data["musicGender"] = test.musicGender
        test_data["sport"] = test.sport
        test_data["hobbie"] = test.hobbie
        test_data["movieSeries"] = test.movieSeries
        test_data["filmGender"] = test.filmGender
        test_data["tabaco"] = test.tabaco
        test_data["alcohol"] = test.alcohol
        test_data["party"] = test.party
        test_data["ordenConvivencia"] = test.ordenConvivencia
        test_data["ordenPersonal"] = test.ordenPersonal
        test_data["personalidad"] = test.personalidad
        output.append(test_data)

    return jsonify({"tests": output})

# get all test  hombre
@app.route("/api/test/Hombre", methods=["GET"])
@token_required
def get_all_test_men(current_user):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"})

    tests = TestR.query.filter_by(gender="masculino").all()

    output = []

    for test in tests:
        test_data = {}
        resident = Residents.query.filter_by(public_id=test.public_id).first()
        test_data["resident_id"] = resident.id
        test_data["gender"] = test.gender
        test_data["age"] = test.age
        test_data["musicGender"] = test.musicGender
        test_data["sport"] = test.sport
        test_data["hobbie"] = test.hobbie
        test_data["movieSeries"] = test.movieSeries
        test_data["filmGender"] = test.filmGender
        test_data["tabaco"] = test.tabaco
        test_data["alcohol"] = test.alcohol
        test_data["party"] = test.party
        test_data["ordenConvivencia"] = test.ordenConvivencia
        test_data["ordenPersonal"] = test.ordenPersonal
        test_data["personalidad"] = test.personalidad
        output.append(test_data)

    return jsonify({"tests": output})

# get all test  Mujer
@app.route("/api/test/Mujer", methods=["GET"])
@token_required
def get_all_test_female(current_user):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"})

    tests = TestR.query.filter_by(gender="femenino").all()

    output = []

    for test in tests:
        test_data = {}
        resident = Residents.query.filter_by(public_id=test.public_id).first()
        test_data["resident_id"] = resident.id
        test_data["gender"] = test.gender
        test_data["age"] = test.age
        test_data["musicGender"] = test.musicGender
        test_data["sport"] = test.sport
        test_data["hobbie"] = test.hobbie
        test_data["movieSeries"] = test.movieSeries
        test_data["filmGender"] = test.filmGender
        test_data["tabaco"] = test.tabaco
        test_data["alcohol"] = test.alcohol
        test_data["party"] = test.party
        test_data["ordenConvivencia"] = test.ordenConvivencia
        test_data["ordenPersonal"] = test.ordenPersonal
        test_data["personalidad"] = test.personalidad
        output.append(test_data)

    return jsonify({"tests": output})

#Hacer la IA para todos los residentes 
@app.route("/api/ia/matchs", methods=["GET"])
# @token_required
# def get_all_test(current_user):
def matchs_ia():

    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    tests = TestR.query.all()

    dataSet = []
    trans_tab = dict.fromkeys(map(ord, u"\u0301\u0308"), None)
    for test in tests:
        # test_data = {}
        resident = Residents.query.filter_by(public_id=test.public_id).first()
        test_data = (
            str(resident.id)
            + "-"
            + test.gender
            + str(test.age)
            + test.musicGender
            + test.sport
            + test.hobbie
            + test.movieSeries
            + test.filmGender
            #+ test.tabaco
            #+ test.alcohol
           # + test.party
           # + str(test.ordenConvivencia)
           # + str(test.ordenPersonal)
            + test.personalidad
        )
        test_data = normalize("NFKC", normalize("NFKD", test_data).translate(trans_tab))
        dataSet.append(test_data)

    distans = [
        distance.edit_distance(dataSet[i], dataSet[j])
        for i in range(1, len(dataSet))
        for j in range(0, i)
    ]

    labels, error, nfound = PC.kmedoids(distans, nclusters=2, npass=1000)
    cluster = dict()
    output = []
    for roommate, label in zip(dataSet, labels):
        cluster.setdefault(label, []).append(roommate)
    for label, grp in cluster.items():
        cluster_data = {}
        cluster_data["Roommate"] = grp
        cluster_data["label"] = str(label)
        output.append(cluster_data)

    return jsonify({"testsALL": output}, {"error": error}, {"nfound": nfound})

#Hacer los emparejamientos para hombres

@app.route("/api/ia/matchsHombres", methods=["GET"])
# @token_required
# def get_all_test(current_user):
def matchs_ia_hombres():

    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    tests = TestR.query.filter_by(gender="masculino").all()

    dataSet = []
    #Quitar asentos, ñ , etc..
    trans_tab = dict.fromkeys(map(ord, u"\u0301\u0308"), None)
    for test in tests:
        resident = Residents.query.filter_by(public_id=test.public_id).first()
        test_data = (
            str(resident.id)
            + "-"
            #+ test.gender
            + str(test.age)
            + test.musicGender
            + test.sport
            + test.hobbie
            + test.movieSeries
            + test.filmGender
            + test.tabaco
            + test.alcohol
            + test.party
            + str(test.ordenConvivencia)
            + str(test.ordenPersonal)
            + test.personalidad
        )
        test_data = normalize("NFKC", normalize("NFKD", test_data).translate(trans_tab))
        dataSet.append(test_data)

    distans = [
        distance.edit_distance(dataSet[i], dataSet[j])
        for i in range(1, len(dataSet))
        for j in range(0, i)
    ]

    labels, error, nfound = PC.kmedoids(distans, nclusters=3, npass=100)
    cluster = dict()
    output = []
    for roommate, label in zip(dataSet, labels):
        cluster.setdefault(label, []).append(roommate)
    for label, grp in cluster.items():
        cluster_data = {}
        cluster_data["Roommate"] = grp
        cluster_data["label"] = str(label)
        output.append(cluster_data)

    return jsonify({"testsHombres": output}, {"error": error}, {"nfound": nfound})

#Hacer los emparejamientos para mujeres

@app.route("/api/ia/matchsMujeres", methods=["GET"])
# @token_required
# def get_all_test(current_user):
def matchs_ia_mujeres():

    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    tests = TestR.query.filter_by(gender="femenino").all()

    dataSet = []
    #Quitar asentos, ñ , etc..
    trans_tab = dict.fromkeys(map(ord, u"\u0301\u0308"), None)
    for test in tests:
        resident = Residents.query.filter_by(public_id=test.public_id).first()
        test_data = (
            str(resident.id)
            #+ test.gender
            + str(test.age)
            + test.musicGender
            + test.sport
            + test.hobbie
            + test.movieSeries
            + test.filmGender
            + test.tabaco
            + test.alcohol
            + test.party
            + str(test.ordenConvivencia)
            + str(test.ordenPersonal)
            + test.personalidad
        )
        test_data = normalize("NFKC", normalize("NFKD", test_data).translate(trans_tab))
        dataSet.append(test_data)

    distans = [
        distance.edit_distance(dataSet[i], dataSet[j])
        for i in range(1, len(dataSet))
        for j in range(0, i)
    ]

    labels, error, nfound = PC.kmedoids(distans, nclusters=3, npass=100)
    cluster = dict()
    output = []
    for roommate, label in zip(dataSet, labels):
        cluster.setdefault(label, []).append(roommate)
    for label, grp in cluster.items():
        cluster_data = {}
        cluster_data["Roommate"] = grp
        cluster_data["label"] = str(label)
        output.append(cluster_data)

    return jsonify({"testsMujeres": output}, {"error": error}, {"nfound": nfound})



# make a room
@app.route("/api/room", methods=["POST"])
@token_required
def create_room(current_user):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"})

    data = request.get_json()

    new_room = Rooms(state=data["state"])

    db.session.add(new_room)
    db.session.commit()

    return jsonify({"message": "New room created !"})

# update state of room
@app.route("/api/room/<room_id>", methods=["PUT"])
@token_required
def update_state_room(current_user, room_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"}), 401

    room = Rooms.query.filter_by(id=room_id).first()

    if not room:
        return jsonify({"message": "No room found!"})

    data = request.get_json()

    room.state = data["state"]
    db.session.commit()

    return jsonify({"message": " Rooms state update :D!"})


# End point Get resultados de una habitación table rooms
@app.route("/api/room/<room_id>", methods=["GET"])
@token_required
def get_room_residents(current_user, room_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"}), 401

    room = Rooms.query.filter_by(id=room_id).first()

    if not room:
        return jsonify({"message": "No room found!"})

    room_data = {}
    room_data["roomID"] = room.id
    room_data["State"] = room.state

    return jsonify({"Room": room_data})


# End point get all rooms from rooms table
@app.route("/api/room", methods=["GET"])
@token_required
def get_all_rooms(current_user):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"}), 401

    rooms = Rooms.query.all()

    output = []

    for room in rooms:
        room_data = {}
        room_data["roomID"] = room.id
        room_data["State"] = room.state
        output.append(room_data)

    return jsonify({"rooms": output})


# agregar resident a una habitación o asociar una habitación a un resident
# post
@app.route("/api/match/<room_id>/<public_id>", methods=["POST"])
@token_required
def add_room_to_resident(current_user, room_id, public_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"})

    room = Rooms.query.filter_by(id=room_id).first()

    if not room:
        return jsonify({"message": "No room found!"}), 404

    resident = Residents.query.filter_by(public_id=public_id).first()
    if not resident:
        return jsonify({"message": "Dude, no resident found ! :("}), 404

    new_match = Matches(user_id=resident.public_id, room_id=room.id)
    db.session.add(new_match)
    db.session.commit()

    return jsonify({"message": "New match add!"})

# End point dar los resultados en tabla matchets con id room
@app.route("/api/match/<room_id>", methods=["GET"])
@token_required
def get_matchs_room(current_user, room_id):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"}), 401

    room = Rooms.query.filter_by(id=room_id).first()

    if not room:
        return jsonify({"message": "Dude, no room found"}), 404

    matchR = Matches.query.filter_by(room_id=room.id).first()
    if not matchR:
        return jsonify({"message": "Dude, no room in matchs table"}), 404

    matchAll = Matches.query.filter_by(room_id=room.id).all()

    output = []

    for match in matchAll:
        match_data = {}
        resident = Residents.query.filter_by(public_id=match.user_id).first()
        match_data["room_id"] = match.room_id
        match_data["Resident Name"] = resident.name
        match_data["Resident Last Name"] = resident.lastName
        output.append(match_data)

    return jsonify({"matches": output})




@app.route("/api/ia", methods=["GET"])
# @token_required
def test_ia():
    t0 = time.process_time_ns()
    DataSetTFG = [
        "21HombreElectronicaVolleyballVideojuegosPeliculasThrillerIntrovertid@",
        "25HombreElectronicaFutbolVideojuegosAmbasAccionExtrovertid@",
        "20MujerTodoSurfGuitarraSeriesThrillerExtrovertid@",
        "23HombreHip hopNingunoFiestaSeriesComediaExtrovertid@",
        "21MujerTrapNingunoPasar tiempo en la naturaleza AmbasRomanticas Extrovertid@",
        "20MujerRockTennisTocar guitarraPeliculasComediaIntrovertid@",
        "19MujerTechnoGimnasiaFotografiaSeriesTerrorExtrovertid@",
        "23HombreMetalCalisteniaBateria SeriesComedia Introvertid@",
        "21HombrePopCriketEstudiarPeliculasDramaIntrovertid@",
        "22MujerRockBaloncestoCervezaAmbasThrillerExtrovertid@",
        "25HombreReggeaton Surf Videojuegos SeriesAccion Extrovertid@",
        "22MujerChillVolleyball LeerAmbasAccion Extrovertid@",
        "21MujerReggaetonVolleyballTocar el saxofon AmbasComedia Extrovertid@",
        "19MujerReggaeton VolleyballPasar con amigos AmbasRom-comsExtrovertid@",
        "23MujerPopGimnasioLas peliculasAmbasSuspenseExtrovertid@",
        "21MujerReggaetonNatacionNetflix SeriesThrillerIntrovertid@",
        "21MujerPopEjercicio en casaEscribirSeriesAccionExtrovertid@",
        "22MujerPopSenderismoSalir a tomar algoSeriesSitcomsExtrovertid@",
        "21MujerHeavy metalNatacionScrapbookingAmbasSitcomsIntrovertid@",
        "21MujerRapGimnasioMuchos AmbasThrillerExtrovertid@",
        "22MujerHardcoreYogaFotografia PeliculasThrillerIntrovertid@",
        "22HombrePopDeportes de montanaLa montanaAmbasComedia Extrovertid@",
        "22MujerIndieNingunoCineAmbasDramaExtrovertid@",
        "20MujerPopGimnasioHobbieSeriesComediaExtrovertid@",
        "20MujertechnoNingunoReposteriaAmbasAmorIntrovertid@",
        "20MujerPopCorrer Tejer SeriesComedias Extrovertid@",
        "21MujerNo tengoGimansioLeerAmbasTerrorIntrovertid@",
        "22MujerPopRugbyCineAmbasThriller Extrovertid@",
        "21MujerPopNatacion BaileAmbasRomanticas Introvertid@",
        "21MujerPopNinguno LeerAmbasRomanticas Extrovertid@",
        "22MujerReggaeton Ninguno Ver series SeriesDrama Introvertid@",
        "22MujerNo tengo Ninguno BailarAmbasCiencia ficcion Extrovertid@",
        "22MujerNo tengo Ninguno BailarAmbasCiencia ficcion Extrovertid@",
        "20MujerPopGimnasioCocinarAmbasDrama Extrovertid@",
        "25HombreIndieVolleyballGamingSeriesDibujos animadosIntrovertid@",
        "17MujerIndieVolleyballVideojuegos AmbasHistoria Introvertid@",
        "23MujerPopPole danceBailarAmbasComediaExtrovertid@",
        "19MujerRockBaileLeer AmbasDramaIntrovertid@",
        "20MujerIndieNingunoCantarAmbasTerrorIntrovertid@",
        "21MujerPopNingunoCantarAmbasRomanceIntrovertid@",
        "21MujerPopDanzaLeerAmbasPoliciacasExtrovertid@",
        "23MujerRockNingunoIdiomas AmbasSuspensoExtrovertid@",
        "23HombrePunkAtletismo Dibujo SeriesDramaIntrovertid@",
        "20MujerRockTennisTocar guitarraPeliculasComediaIntrovertid@",
        "21MujerPopPilatesLeerAmbasMisterioExtrovertid@",
        "25MujerPopNingunoTeatroAmbasThrillerExtrovertid@",
        "19MujerElectronica Tocho bandera Tocho Bandera AmbasAccion Introvertid@",
        "18MujerPopSenderismoEstar con mi familia SeriesDrama Extrovertid@",
        "23Hombreindie NingunoFotografiaAmbasAccion Introvertid@",
        "21MujerIndieVolleyballLeerAmbasRom-comsIntrovertid@",
        "21MujerIndieNatacionEstar al aire libreSeriesRomanticasIntrovertid@",
        "20MujerR&BCrossFitHacer ejercicioPeliculasSuspensoIntrovertid@",
        "19MujerPopNingunoLa musicaPeliculasRomanticasExtrovertid@",
        "19MujerIndieTenniscocinar AmbasSuspensoExtrovertid@",
        "19HombreSkaFutbolPcAmbasAccionIntrovertid@",
        "18HombreRapNingunoLeerAmbasMisterioIntrovertid@",
        "22MujerIndieNingunoDibujarAmbasSuspensoIntrovertid@",
        "20HombreTodoVolleyball EscribirAmbasDramaExtrovertid@",
        "20HombreTodoFutbolLeerAmbasAccion Extrovertid@",
        "22MujerPop NingunoPasar con mi familiaAmbasRom-comsExtrovertid@",
        "20HombreTechnoCrossfitVer seriesAmbasAccion Introvertid@",
        "22HombreRapFutbol Fotografia PeliculasThrillerIntrovertid@",
        "21MujerRockVolleyball La musica PeliculasComediaExtrovertid@",
        "19MujerElectronica Tocho bandera Tocho Bandera AmbasAccion Introvertid@",
        "25HombreRockFutbol Fotografia AmbasComedia Extrovertid@",
        "20MujerRockTennisTocar guitarraPeliculasComediaIntrovertid@",
        "21MujerReggaetonVolleyballTocar el saxofon AmbasSuspenso Extrovertid@",
        "21MujerElectronica Futbol EscribirAmbasAnimeExtrovertid@",
        "21MujerReggaetonVolleyballEscuchar musica AmbasAccion Extrovertid@",
        "21MujerIndieBaseballTocar el saxofon AmbasSuspensoExtrovertid@",
        "21HombreCorridosFutbolVideojuegosPeliculasTerrorIntrovertid@",
        "22HombreHouseGolfVideojuegosSeriesSuspensoExtrovertid@",
        "21MujerPopNinguno Dibujar AmbasAnimeIntrovertid@",
        "24HombreReggaeton Futbol Jugar a la consolaAmbasAccion Extrovertid@",
        "20MujerReggaeton NingunoEscuchar musica PeliculasComediaExtrovertid@",
        "25HombreTech HouseNingunoe-sportsAmbasTerror PsicologicoIntrovertid@",
        "24HombreRockFutbolHacer deporte AmbasSuspenso Introvertid@",
        "21HombreReaggeton BaseballVer peliculas AmbasComediaExtrovertid@",
        "25HombreMetalFutbol GymAmbasThrillerIntrovertid@",
        "25HombrePunkFutbolEl GimnasioSeriessuspensoExtrovertid@",
        "22HombreRapFutbolHacer ejercicio AmbasAccionExtrovertid@",
        "21MujerPopHitDibujarAmbasRomanceExtrovertid@",
        "25HombreBandaFutbol VideojuegosAmbasTodosIntrovertid@",
        "19MujerFlamenco BaileHobbieSeriesCriminal Extrovertid@",
        "23HombreTrap CiclismoJugar Xbox AmbasComedia Extrovertid@",
        "24HombreSalsaFutbolVideojuegosSeriesMisterioIntrovertid@",
        "25HombreUrbanoRunningDeportesPeliculasPolicialIntrovertid@",
        "22HombreReggaeton Futbol Cocinar AmbasAccion Extrovertid@",
        "22HombreRock FutbolGimnasioAmbasThrillerExtrovertid@",
        "19MujerR&BNingunoLeerPeliculasAccion Introvertid@",
        "19MujerPop NingunoBailarAmbasAmorExtrovertid@",
        "20MujerPopNingunoEstudiar japones PeliculasTerror Introvertid@",
        "20MujerReggaeton Ninguno CocinarAmbasRomanticas Extrovertid@",
        "19MujerLatinoVolleyball Estar con amigosAmbasComedia Extrovertid@",
        "24MujerReggaetonGimnasia RitmicaViajarPeliculasSuspenseIntrovertid@",
        "19MujerPopTennisLeerAmbasAccion Introvertid@",
        "20MujerR&BVolleyballDibujarAmbasComediasIntrovertid@",
        "19MujerAlternativoEsgrimaMusicaSeriesCrimenIntrovertid@",
        "20MujerRockNinguno Cantar AmbasRom-comsIntrovertid@",
        "19MujerRockKarateDibujarAmbasRom-comsIntrovertid@",
        "19MujerIndependiente AtletismoCocinarAmbasRom-comsExtrovertid@",
        "20MujerElectro latinoVolleyballLeerPeliculasRom-comsExtrovertid@",
        "19MujerPopNingunoCorrerSeriesComediaExtrovertid@",
        "19MujerPop EsgrimaTocar violin AmbasComediaIntrovertid@",
        "20MujerPopVolleyball LeerAmbasAccionIntrovertid@",
        "21MujerPopNinguno Dibujar AmbasAnimeIntrovertid@",
        "19MujerPopNingunoCorrerSeriesComediaExtrovertid@",
        "19MujerPopNingunoVer seriesSeriesComediaExtrovertid@",
        "25HombreBandaFutbol VideoJuegosAmbasTodosIntrovertid@",
        "19MujerReggaetonNingunoleerSeriescrimenExtrovertid@",
        "19MujerPopGymLeerSeriesDramaExtrovertid@",
        "19MujerPopNo practico LeerPeliculasRomanticasExtrovertid@",
        "20MujerPopNingunoLeerSeriesRomanticasExtrovertid@",
        "24HombreRockFutbolHacer deporte AmbasSuspenso Introvertid@",
        "25HombreEDMGymPatinar con long AmbasComedia Extrovertid@",
        "19MujerReggaetonNingunoleerSeriescrimenExtrovertid@",
        "19MujerRapNadaToco guitarraSeriesComedia Extrovertid@",
        "22HombreReggaeton Futbol Cocinar AmbasAccion Extrovertid@",
        "25HombreMoombathonGimnasioDjPeliculasAccion Extrovertid@",
        "25HombreBandaFutbol VideoJuegosAmbasTodosIntrovertid@",
        "22HombreRockFutbolGimnasioAmbasCiencia ficcion Extrovertid@",
        "21MujerPopRunningDormirAmbasRomanticasIntrovertid@",
        "20MujerReggaetonGimnasioBaileSeriesCiencia ficcion Extrovertid@",
        "19HombrePopFutbolLeerSeriesFantasiaIntrovertid@",
        "19MujerRockYogaCineAmbasComedia romanticaExtrovertid@",
        "18MujerRapJudoLa montanaPeliculasComediaExtrovertid@",
        "19MujerPopZumbaVer seriesSeriesDrama Extrovertid@",
        "18MujerNingunoBaloncesto DeportePeliculasDramaIntrovertid@",
        "19HombreTrapBaloncestoBaloncestoAmbasSuspenseExtrovertid@",
        "19MujerPopDeporte en casaEscuchar musicaSeriesAmor adolescenteExtrovertid@",
        "18MujerPopNinguno Ver seriesSeriesDramaIntrovertid@",
        "18HombrePopCaminar DocumentalesSeriesIntriga Introvertid@",
        "19MujerIndieGimnasioLeerSeriesRomanticasIntrovertid@",
        "20MujerPopBaloncesto LeerSeriesSuspensoIntrovertid@",
        "19HombreElectronicaCorrerCocinarPeliculasCiencia ficcionIntrovertid@",
        "18MujerPopAtletismoMusicaAmbasThrillerIntrovertid@",
        "20HombreHip hopNatacionSenderismoAmbasAccionExtrovertid@",
        "21MujerIndie Andar MusicaSeriesAccionExtrovertid@",
        "21MujerIndieGimnasioLeerSeriesDramaIntrovertid@",
        "19MujerPopVolleyballCorrerAmbasAccionIntrovertid@",
        "18MujerRockNingunoBailarAmbasMisterioIntrovertid@",
        "21MujerNo tengo Correr Maquillaje AmbasComedia Introvertid@",
        "19HombreTrapBaloncestoBaloncestoAmbasSuspensoExtrovertid@",
        "18MujerPopAerobicEl movilSeriesPoliciacasExtrovertid@",
        "25MujerRockCapoeiraViajarAmbasComedia Extrovertid@",
        "18MujerPopCiclismoLeerSeriesMedicasIntrovertid@",
        "19MujerIndieNingunoVer seriesSeriesComediaIntrovertid@",
        "19MujerRapGimnasioCosturaSeriesMisterio Extrovertid@",
        "20HombreRockGimnasioLeerPeliculasHumorExtrovertid@",
        "20MujerPopVelaMusicaSeriesJuvenilIntrovertid@",
        "22MujerSalsaFutbol CosturaPeliculasComediaExtrovertid@",
        "18HombrePopFutbol Futbol AmbasCiencia ficcion Extrovertid@",
        "20HombreTodoFutbol PlayStation SeriesDrama crimen Introvertid@",
        "19HombreElectronica Futbol PlayStation AmbasCiencia Ficcion Introvertid@",
        "24HombreBaladas FutbolNetflix SeriesComedias romanticas Extrovertid@",
        "19HombreTrapFutbol Video juegos AmbasComedia Introvertid@",
        "20HombreReggaetonFutbol DibujarAmbasMisterioExtrovertid@",
        "19HombreElectronica Futbol PlayStation AmbasTerrorExtrovertid@",
        "22MujerPopVolleyball LeerAmbasRom-comsExtrovertid@",
        "20HombrePopFootballDeportesSeriesMisterioExtrovertid@",
        "19HombreReggaeton Futbol PlayStation AmbasCiencia ficcion Introvertid@",
        "20HombreMusica urbanaVolleyball Videojuegos AmbasMisterioIntrovertid@",
        "19HombreReguetonTennisVideojuegosSeriesDramaIntrovertid@",
        "25HombreRockFutbolVer series SeriesThrillerExtrovertid@",
        "20HombreReggaetonVolleyballDibujarPeliculasTodasExtrovertid@",
        "19HombreElectronicaFutbolProgramarSeriesSuspensoExtrovertid@",
        "20MujerUrbano PescaCocinarPeliculasComediaExtrovertid@",
        "22HombrePopFutbol Futbol AmbasMisterioIntrovertid@",
        "18HombreRockFutbolNetflixPeliculasTerrorExtrovertid@",
        "20HombreRapFutbolVideojuegosSeriesComediaIntrovertid@",
        "18HombreElectronica Futbol PlayStation AmbasAccion Extrovertid@",
        "20HombreIndieFutbolEscuchar musicaAmbasDramaExtrovertid@",
        "18HombreElectronica Futbol PlayStation AmbasAccion Extrovertid@",
        "19MujerPopYogaLeerSeriesDramaExtrovertid@",
        "22HombrePopFutbol Futbol AmbasMisterioIntrovertid@",
        "25HombreEDMGymPatinar con long AmbasComedia Extrovertid@",
        "21MujerIndieGimnasioNetflixAmbasIntrigaIntrovertid@",
        "19MujerPopAtletismoViajarPeliculasIntrigaIntrovertid@",
        "25MujerRockCapoeiraViajarAmbasComedia Extrovertid@",
        "22MujerRockNatacionCantarSeriesMisterioIntrovertid@",
        "22HombreRap Futbol PlayStation AmbasComedia Extrovertid@",
        "19MujerReggaetonNingunoLeerSeriesIntrigaExtrovertid@",
        "20MujerPopEjercicio en casaLeerAmbasRomanticasExtrovertid@",
        "21HombreSalsaVolleyball CorrerSeriesAccionIntrovertid@",
        "19MujerIndieYogaLeerSeriesMisterioExtrovertid@",
        "22MujerReggaetonVolleyball LeerAmbasDramaIntrovertid@",
        "20MujerCorridosNinguno Tocho Bandera AmbasMisterioExtrovertid@",
        "20MujerElectronicaFutbol ViajarSeriesComedias romanticas Introvertid@",
        "21MujerPopNingunoDibujarAmbasSuspensoExtrovertid@",
        "19HombreIndiePilatesEl movilSeriesCriminal Extrovertid@",
        "20MujerTechnoFutbol Videojuegos PeliculasTodasExtrovertid@",
        "20MujerLatinoCapoeiraPcAmbasAccion Extrovertid@",
        "24MujerChillGimnasioCosturaPeliculasTerrorExtrovertid@",
        "25MujerPop YogaLeerSeriesFantasiaExtrovertid@",
        "24HombrePopCorrer ViajarAmbasComedia Extrovertid@",
        "21MujerPopFutbol LeerAmbasComediaExtrovertid@",
        "20HombrePopBaileLeerAmbasAccionExtrovertid@",
        "22HombreEDMFutbolVer seriesPeliculasAccion Extrovertid@",
        "25MujerRockNingunoHobbieAmbascrimenExtrovertid@",
        "24MujerMusica urbanaNingunoleerAmbasSuspensoIntrovertid@",
        "18MujerPopVolleyball CocinarPeliculasCiencia ficcionExtrovertid@",
        "21MujerR&BNinguno PlayStation SeriesThrillerIntrovertid@",
        "23MujerRockGimnasiaLeerAmbasComedia Introvertid@",
        "22MujerTrapHitLeer PeliculasDramaExtrovertid@",
        "25MujerReggeaton RunningLeerSeriesDramaIntrovertid@",
        "20HombrePopNingunoTocar el saxofon AmbasSuspensoExtrovertid@",
        "22MujerPopNingunoReposteriaPeliculasComediaExtrovertid@",
        "19HombreTrapFutbolLeerSeriesThriller Extrovertid@",
        "21MujerPopFutbolBateria AmbasComediaIntrovertid@",
        "20HombreRapGimnasioLeerSeriesThrillerIntrovertid@",
        "22HombreR&BFutbol CocinarSeriesRomanceIntrovertid@",
        "25HombreReggaetonNingunoBaileAmbasAccion Extrovertid@",
        "18MujerReggaeton DanzaCorrerSeriesRom-comsExtrovertid@",
        "21MujerMetalGymFotografiaPeliculasMisterioExtrovertid@",
        "23MujerElectronica Volleyball CineAmbasMisterio Introvertid@",
        "22MujerRockBaseballJugar a la consolaPeliculasPoliciacasExtrovertid@",
        "23MujerR&BNingunoDormirAmbasComedia Extrovertid@",
        "19MujerPopNadaScrapbookingAmbasSuspenso Introvertid@",
        "20MujerPopFutbol GimnasioAmbasAccion Introvertid@",
        "19HombreRockFutbol Dibujar AmbasAmorExtrovertid@",
        "19HombreRockNingunoMusicaAmbasSuspensoExtrovertid@",
        "22MujerEDMFutbol Dibujar AmbasComedia Introvertid@",
        "21MujerPopFutbol LeerAmbasAccion Introvertid@",
        "20HombrePopFootballLeerAmbasComedia Extrovertid@",
        "19HombreRockZumbaVer seriesSeriesTerrorExtrovertid@",
        "19HombreReggaetonBaileBaloncestoSeriesCiencia ficcion Extrovertid@",
        "19MujerPopFutbolToco guitarraSeriesComedia romanticaExtrovertid@",
        "22HombreReggaeton Tocho bandera Escuchar musica AmbasMisterioExtrovertid@",
        "25MujerNo tengoNatacionTocar violin SeriesDramaExtrovertid@",
        "19HombrePopNatacionLa montanaSeriesIntrigaExtrovertid@",
        "19MujerPopNingunoVer seriesAmbasAccion Introvertid@",
        "20MujerPopNingunoFotografia AmbasAccionIntrovertid@",
        "21MujerRock Futbol NetflixAmbasAccionExtrovertid@",
        "18HombreElectronica TennisVer series SeriesDramaIntrovertid@",
        "21HombrePopFutbolCocinar AmbasRomanticasIntrovertid@",
        "22HombreElectronicaVolleyballJugar Xbox SeriesMisterioExtrovertid@",
        "22HombrePopGimnasia RitmicaLa montanaSeriesTerrorIntrovertid@",
        "18MujertechnoRugbyNetflixAmbasComediaIntrovertid@",
        "21MujerTrapVolleyballFotografiaAmbasDramaIntrovertid@",
        "19MujerElectronicaNatacionEscuchar musicaAmbasCrimenExtrovertid@",
        "22MujerRapFutbolPlayStation SeriesRomanticasExtrovertid@",
        "21HombreElectronica GolfCocinar AmbasRomanticasExtrovertid@",
        "18HombreReggaeton NingunoSalir a tomar algoAmbasCiencia ficcion Extrovertid@",
        "21MujerTech HouseCiclismoLeerAmbasTerror Introvertid@",
        "22HombrePunkFutbol LeerAmbasSuspenseExtrovertid@",
        "21HombreRapCalisteniaPlayStation PeliculasCiencia ficcion Introvertid@",
        "18MujerPopNingunoVideo juegos AmbasDrama Introvertid@",
        "20MujerPopAerobicSenderismoSeriesDramaExtrovertid@",
        "20MujerUrbano GimansioGymAmbasSuspensoExtrovertid@",
        "19MujerPopNatacionLeerSeriesComediaExtrovertid@",
        "22MujerRockNingunoTocar guitarraAmbasAccionExtrovertid@",
        "21HombreElectro latinoNinguno DeportesSeriesRom-comsIntrovertid@",
        "20HombreBandaDeportes de montanae-sportsPeliculasDrama Introvertid@",
        "22MujerReggaetonNinguno DibujarAmbasAccion Extrovertid@",
        "20MujerSalsaFutbol Estudiar japones SeriesComediaExtrovertid@",
        "19MujerRockNingunoFutbol SeriesMedicasIntrovertid@",
        "18MujerIndieFutbol Ver series AmbasSuspensoIntrovertid@",
        "22HombrePopPescaCantar AmbasCiencia ficcion Extrovertid@",
        "22MujerIndieBaloncestoLeerPeliculasAccionExtrovertid@",
        "20HombreNingunoSurf GuitarraPeliculasTerrorExtrovertid@",
        "19MujerPopNingunoCantarSeriesTodosIntrovertid@",
        "20MujerTrapNingunoCocinarAmbasAmorIntrovertid@",
        "21MujerPopVolleyball DjAmbasAccionIntrovertid@",
        "22MujerPopTennisTeatroSeriescrimenIntrovertid@",
        "19HombreTodoFutbolMusicaPeliculasSuspensoExtrovertid@",
        "21MujerPopFutbolPasar con amigos AmbasRomanticas Introvertid@",
        "21HombreTrap Volleyball VideojuegosPeliculasThrillerExtrovertid@",
        "19MujerTodoVolleyball LeerPeliculasComediaIntrovertid@",
        "21HombreReggaeton GimnasioVideojuegos AmbasThrillerExtrovertid@",
        "19MujerPopVolleyballLeerAmbasComedia Introvertid@",
        "19MujerRockFutbol ProgramarPeliculasHumorIntrovertid@",
        "21HombreTechnoSenderismoFotografia PeliculasComedia Extrovertid@",
        "21HombreReggaeton FutbolBaloncestoSeriesThrillerExtrovertid@",
        "18MujerRockBaloncestoDeportesAmbasComediaExtrovertid@",
        "19MujerPop Tocho bandera VideojuegosSeriesAccion Introvertid@",
        "20HombreRapTennisNetflix SeriesThrillerExtrovertid@",
        "22MujerPopTennisCocinarSeriesPoliciacasIntrovertid@",
        "25HombreIndieVelaVideojuegosSeriesComediaExtrovertid@",
        "21HombreRapGimnasioDibujarAmbasRomanticasExtrovertid@",
        "25HombreIndieGimnasioBailarSeriesTodosIntrovertid@",
        "20HombreMetalGimnasioHobbieAmbasAccion Introvertid@",
        "25MujerReggaetonVolleyballVideojuegosAmbasAccion Introvertid@",
        "20MujerTodoFutbolBailarAmbasComedia Extrovertid@",
        "19HombreAlternativoFutbol DibujarAmbasComediaExtrovertid@",
        "19HombreRockNingunoVideoJuegosAmbasComediaExtrovertid@",
        "20MujerIndependiente CapoeiraPlayStation AmbasComedia Introvertid@",
        "20MujerBandaFutbol VideojuegosAmbasRom-comsExtrovertid@",
        "19MujerPopBaloncesto Escuchar musica AmbasDramaIntrovertid@",
        "25MujerRapFutbol LeerAmbasMisterioIntrovertid@",
        "20HombrePopFutbolEscribirAmbasRom-comsIntrovertid@",
        "25HombrePopCrossFitVideojuegosAmbasTodosExtrovertid@",
        "24MujerElectronica Futbol LeerPeliculasThrillerIntrovertid@",
        "19MujerReguetonVolleyballTocar guitarraAmbasComedia Introvertid@",
        "23HombrePopRunningDeporteAmbasTerrorExtrovertid@",
        "19HombreRockBaloncestoBailarPeliculasIntrigaExtrovertid@",
        "20MujerRockVolleyballEscribirSeriesRomanticasIntrovertid@",
        "21MujerReggaeton Deporte en casaFutbol AmbasSitcomsExtrovertid@",
        "19MujerPopEsgrimaHacer ejercicio AmbasRom-comsIntrovertid@",
        "19HombreRapNinguno Patinar con long AmbasComediaExtrovertid@",
        "19HombreReggaetonGymVideojuegos AmbasComedia Extrovertid@",
        "19HombreElectronica VolleyballMaquillaje SeriesRomanticas Extrovertid@",
        "19MujerSkaNinguno Ver seriesSeriesRomanticas Extrovertid@",
        "21MujerPopNingunoViajarSeriesSuspenseIntrovertid@",
        "18HombrePunkFutbolPasar con mi familiaAmbasComedia Extrovertid@",
        "18MujerHip hopNingunoHacer deporte SeriesAccion Extrovertid@",
        "18MujerRockAndar DibujarAmbasDibujos animadosIntrovertid@",
        "22MujerRockNingunoMuchos AmbasDramaExtrovertid@",
        "19HombreReggaetonTennisGimnasioAmbasThrillerIntrovertid@",
        "24MujerHip hopNingunoPlayStation SeriesSuspenso Introvertid@",
        "21MujerHeavy metalAtletismoLeerAmbasDrama Extrovertid@",
        "19MujerPopFutbolVideojuegosSeriesRom-comsIntrovertid@",
        "19MujerReggaeton JudoMusicaAmbasTerror PsicologicoIntrovertid@",
        "20Mujerindie VolleyballCineAmbasCiencia Ficcion Extrovertid@",
        "21MujerIndieGimnasioEscuchar musicaSeriesAccion Introvertid@",
        "18HombrePopNingunoTocho Bandera AmbasSuspenso Extrovertid@",
        "25MujerNo tengo GimnasioLeerPeliculasRom-comsExtrovertid@",
        "22MujerRapPole danceMusicaAmbasComediaExtrovertid@",
        "25HombreIndieNingunoGamingSeriesComediaExtrovertid@",
        "23HombreIndieFutbolPlayStation AmbasSitcomsExtrovertid@",
        "19HombreRockNingunoFotografia AmbasHistoria Extrovertid@",
        "22MujerUrbanoEsgrimaCantarAmbasComediaExtrovertid@",
        "19MujerPop CiclismoTocar guitarraSeriesAnimeIntrovertid@",
        "22MujerRockNingunoEstudiarAmbasRomanticas Introvertid@",
        "21MujerPopSenderismoLa musica PeliculasAccionIntrovertid@",
        "20MujerPopYogaDibujarAmbasComedia Introvertid@",
        "17MujerElectronica NingunoTocar el saxofon AmbasThrillerExtrovertid@",
        "21MujerPopBaseballPasar tiempo en la naturaleza SeriesSuspenseIntrovertid@",
        "20MujerRap Futbol VideoJuegosAmbasDramaIntrovertid@",
        "18HombreIndieAtletismoFutbol PeliculasThrillerExtrovertid@",
        "20MujerBandaFutbolHacer deporte PeliculasComediaExtrovertid@",
        "22MujerNo tengo Futbol PlayStation AmbasAccion Introvertid@",
        "25MujerTodoCorrer Ver seriesAmbasMisterioIntrovertid@",
        "19MujerReggaetonCrossfitEstar con mi familia AmbasThrillerExtrovertid@",
        "25MujerFlamenco NingunoFiestaAmbasDrama Introvertid@",
        "22HombreElectronica FutbolEstar al aire libreAmbasIntrigaIntrovertid@",
        "19HombreHouseVolleyballNetflix AmbasComediasExtrovertid@",
        "19MujerRockVolleyballVideojuegosAmbasComedias Introvertid@",
        "23HombrePopNatacionBailarPeliculasRom-comsIntrovertid@",
        "24MujerReaggeton CriketLeerSeriesDramaIntrovertid@",
        "25MujerIndieGimnasioDocumentalesAmbasDramaExtrovertid@",
        "18MujerReggaetonVolleyballHacer ejercicioPeliculasJuvenilExtrovertid@",
        "21HombrePopAtletismoIdiomas AmbasAnimeIntrovertid@",
        "23HombrePopCaminar CorrerAmbasThrillerExtrovertid@",
        "21MujerIndieNinguno cocinar AmbasComediaExtrovertid@",
        "19MujerPopNinguno CineAmbasMisterioExtrovertid@",
        "20MujerPopSurfDibujo AmbasIntriga Extrovertid@",
        "21MujerRockFutbolCantarPeliculasSuspensoIntrovertid@",
        "19HombreRockBaloncesto CocinarPeliculasRomanceIntrovertid@",
        "20HombreBaladas GimnasioPatinar con long AmbasCiencia ficcion Extrovertid@",
        "20MujerElectronicaFutbol Tejer AmbasAccion Introvertid@",
        "23HombreReggaetonCorrerBailarSeriesCiencia ficcion Introvertid@",
        "20MujerMoombathonKarateLeerAmbasAnimeIntrovertid@",
        "19MujerPopFutbol ViajarAmbasComediaExtrovertid@",
        "21MujerNo tengo Natacion Tocar el saxofon SeriesPolicialExtrovertid@",
        "20MujerIndieVolleyballBailePeliculasAccion Extrovertid@",
        "25HombrePopGymCosturaSeriesMisterioExtrovertid@",
        "19MujerIndieTennisLeerSeriessuspensoIntrovertid@",
        "19HombreRockAtletismo Ver peliculas AmbasAccion Introvertid@",
        "20HombreHardcoreFutbolEscribirSeriesComedia Extrovertid@",
        "25MujerReggaetonNo practico El GimnasioSeriesDrama crimen Introvertid@",
        "25MujerReggaeton Ninguno La musicaAmbasAmor adolescenteExtrovertid@",
        "22HombrePopFutbol CervezaSeriesSuspensoExtrovertid@",
        "19HombrePopFutbol Las peliculasSeriesTerrorIntrovertid@",
        "19HombreIndie GimnasioEstar con amigosAmbasMisterioExtrovertid@",
        "21HombrePopNatacion CocinarSeriesThrillerIntrovertid@",
        "20MujerPopTennisTeatroAmbasMisterioIntrovertid@",
        "25HombreNo tengo Futbol Ver seriesAmbasComediaExtrovertid@",
        "25MujerRockFutbolLa musicaSeriesSuspensoIntrovertid@",
        "22MujerRockNingunoCantarAmbasComedia Introvertid@",
        "18MujerNo tengo FutbolLeerSeriesComedias Extrovertid@",
        "22HombreRockVolleyballBailarSeriesTerror PsicologicoExtrovertid@",
        "23HombrePopCiclismoSalir a tomar algoSeriesCiencia Ficcion Extrovertid@",
        "19HombreIndieNingunoEscuchar musica AmbasSuspenso Extrovertid@",
        "20MujerPopCorrerVideojuegosAmbasAccionExtrovertid@",
        "19MujerReggaetonNingunoPlayStation AmbasThrillerExtrovertid@",
        "20MujerReaggeton VolleyballCantar AmbasAccion Extrovertid@",
        "23MujerPopBaloncestoPlayStation SeriesMisterioIntrovertid@",
        "19MujerElectronica AtletismoCineAmbasComedia Extrovertid@",
        "20MujerReggaetonBaloncestoPasar con mi familiaAmbasCiencia ficcion Extrovertid@",
        "22MujerRapTennisMuchos SeriesAccion Introvertid@",
        "21MujerPopGimnasioTocar violin AmbasComediaIntrovertid@",
        "18HombreIndieNinguno FotografiaPeliculasRomanticasExtrovertid@",
        "18MujerReggaeton Futbol Fotografia AmbasComediaExtrovertid@",
        "20HombreBaladas VolleyballPatinar con long AmbasRomanticasExtrovertid@",
        "19HombreTrap Baloncesto Videojuegos AmbasComediaExtrovertid@",
        "19MujerPopVolleyball ViajarSeriesRom-comsIntrovertid@",
        "20HombrePopGimnasioPlayStation AmbasThrillerIntrovertid@",
        "21HombreRockFutbolFutbol AmbasThrillerExtrovertid@",
        "20HombreIndependiente NatacionBailarAmbasRom-comsIntrovertid@",
        "21MujerIndieGimnasioLeerAmbasAccion Extrovertid@",
        "19MujerPopFutbolVideo juegos PeliculasDrama Introvertid@",
        "19HombreUrbano GimnasioTejer SeriesJuvenilIntrovertid@",
        "19MujerNingunoKarateEscuchar musica SeriesSuspensoIntrovertid@",
        "20MujerIndieFutbol CantarSeriesComediaExtrovertid@",
        "22HombreTech HouseGimnasioVer seriesSeriesPoliciacasIntrovertid@",
        "21HombreReggaeton NatacionTocho Bandera AmbasThrillerIntrovertid@",
        "19MujerPopNingunoViajarPeliculasThrillerExtrovertid@",
        "21HombrePopVolleyballPlayStation AmbasRom-comsIntrovertid@",
        "22HombreRockGymVideojuegosSeriesPolicialIntrovertid@",
        "20MujerIndieFutbolVideojuegos PeliculasComediaExtrovertid@",
        "20HombrePopGimnasioEscribirSeriesIntrigaExtrovertid@",
        "19HombreSkaCriketDeporteSeriesTodosIntrovertid@",
        "19HombreIndieNingunoLeerSeriesAccionIntrovertid@",
        "22HombreNo tengoCrossfitEl GimnasioAmbasComediaExtrovertid@",
        "20MujerPopFutbol Ver seriesAmbassuspensoIntrovertid@",
        "18MujerPopEsgrimaDeportesPeliculasMisterioExtrovertid@",
        "22HombrePopNingunoSenderismoAmbasHistoria Introvertid@",
        "20MujerRockAerobicBailarAmbasComediaExtrovertid@",
        "20MujerTechnoNinguno e-sportsPeliculasAccionExtrovertid@",
        "25MujerRapGimansioVideoJuegosPeliculasTerrorIntrovertid@",
        "21MujerRockVolleyballGimnasioPeliculasDrama crimen Introvertid@",
        "21MujerReggaeton Futbol PlayStation SeriesAmor adolescenteExtrovertid@",
        "23MujerRockVelaVer series AmbasRomanticas Extrovertid@",
        "22MujerReggaetonSenderismoHobbieAmbasTerror Introvertid@",
        "21MujerPopCapoeiraLeerPeliculasDramaIntrovertid@",
        "25MujerMoombathonTennisEstudiar japones SeriesRomanceIntrovertid@",
        "22HombrePopNingunoDibujarAmbasIntrigaExtrovertid@",
        "18MujerElectronicaNingunoTocar guitarraSeriesThrillerExtrovertid@",
        "19HombreElectronica TennisCocinar AmbasTerrorIntrovertid@",
        "19HombreRock VolleyballCocinarPeliculasDramaIntrovertid@",
        "25HombreAlternativoNingunoDjSeriesSuspensoIntrovertid@",
        "22HombreRockGimnasiaProgramarSeriesMisterioIntrovertid@",
        "25Mujerindie NingunoVideojuegosAmbasComedia Extrovertid@",
        "21HombreRockYogaLeerSeriesRomanticas Introvertid@",
        "21MujerElectronica NatacionBaloncestoPeliculasSuspensoIntrovertid@",
        "19MujerPop No practico Netflix AmbasComediaExtrovertid@",
        "24MujerSalsaCaminar Futbol SeriesCiencia ficcion Extrovertid@",
        "19HombrePunkSurf Ver series AmbasDramaExtrovertid@",
        "21MujerReggaetonCalisteniaPasar tiempo en la naturaleza PeliculasDramaExtrovertid@",
        "22MujerPopNinguno LeerPeliculascrimenIntrovertid@",
        "18MujertechnoNatacionTocar guitarraAmbasAccion Introvertid@",
        "19HombreRap NingunoDibujo AmbasAccion Extrovertid@",
        "22MujerRapJudoGymSeriesRom-comsIntrovertid@",
        "21MujerElectronicaEsgrimaVideojuegosAmbasCiencia ficcion Extrovertid@",
        "19HombreBandaBaloncesto GuitarraSeriesComedia Introvertid@",
        "19HombreIndieVolleyball Pasar con amigos AmbasComedia Introvertid@",
        "21MujerPopVolleyballBailarAmbasAnimeExtrovertid@",
        "18HombreRockCiclismoEscuchar musicaAmbasAccionExtrovertid@",
        "21MujerPopCrossFitLeerPeliculasDrama Extrovertid@",
        "23HombreHardcoreTocho bandera Estar con amigosAmbasRomanticas Introvertid@",
        "21MujerPopNinguno MusicaAmbasMisterioIntrovertid@",
        "19MujerPopAtletismoTocar el saxofon AmbasTodosIntrovertid@",
        "22MujerIndieFutbol DocumentalesAmbasCiencia ficcion Extrovertid@",
        "20HombrePopPole danceVideojuegosAmbasIntrigaExtrovertid@",
        "21MujerRockNingunoHacer ejercicioSeriesComediasExtrovertid@",
        "20MujerIndieNingunoLas peliculasPeliculasThrillerExtrovertid@",
        "18MujerElectronica SenderismoCorrerAmbasDrama Extrovertid@",
        "25MujerPopFutbolJugar Xbox AmbasAccion Extrovertid@",
        "25HombreIndieGolfPlayStation AmbasComediaIntrovertid@",
        "20MujerPopFutbolNetflixAmbasAccion Introvertid@",
        "19HombreReggaeton NingunoLeerAmbasAccionIntrovertid@",
        "22MujerPopGimnasioLa montanaAmbasComediaIntrovertid@",
        "21MujerBandaNinguno LeerAmbasAccionExtrovertid@",
        "20HombrePopFutbolLeerSeriesDramaIntrovertid@",
        "22HombreTrapTennisVideoJuegosAmbasDramaIntrovertid@",
        "20MujerHousePescaMusicaSeriesCrimenIntrovertid@",
        "25HombrePopFutbol VideojuegosSeriesSuspenseIntrovertid@",
        "19MujerNo tengo FutbolPatinar con long AmbasDibujos animadosExtrovertid@",
        "25MujerElectro latinoNinguno CosturaPeliculasMisterioIntrovertid@",
        "19HombreReggaetonNingunoCervezaAmbasRomanticasExtrovertid@",
        "22HombrePopTocho bandera Hacer deporte SeriesComedia Extrovertid@",
        "21MujerBandaSurfFotografia SeriesDrama Introvertid@",
        "21MujerTodoFutbol NetflixAmbasComediaIntrovertid@",
        "18HombreIndieCorrer Netflix SeriesRomanticas Extrovertid@",
        "19MujerReggaetonGimnasioFiestaAmbasAccion Introvertid@",
        "19HombreElectronicaFutbol CantarAmbasDramaExtrovertid@",
        "19MujerHeavy metalTennisFotografia PeliculasAccion Extrovertid@",
        "21MujerReggaeton FutbolBailarAmbasCiencia ficcion Extrovertid@",
        "19MujerPopFutbol Hacer deporte AmbasDramaExtrovertid@",
        "19HombreTodoVolleyballBailePeliculasMedicasExtrovertid@",
        "20MujerIndieDeporte en casaHacer ejercicio AmbasTodosExtrovertid@",
        "18MujerElectronica Volleyball cocinar AmbasComediaIntrovertid@",
        "19MujerPopNingunoDibujarAmbasTerrorExtrovertid@",
        "20MujerReggaeton FutbolEstudiarAmbasRom-comsIntrovertid@",
        "25HombreHip hopFutbolLeerAmbasSuspenso Introvertid@",
        "25MujerRapFutbolEscribirAmbasSuspensoIntrovertid@",
        "22HombreRapRunningMaquillaje SeriesRom-comsExtrovertid@",
        "17MujerPopVolleyballCocinarAmbasDramaExtrovertid@",
        "20HombreReggaetonFutbol LeerAmbasRomanticasExtrovertid@",
        "19MujerMetalFutbol DeportesSeriesSuspenseIntrovertid@",
        "22MujerRockNingunoLa montanaSeriesHumorExtrovertid@",
        "20MujerRockAndar Estar al aire libreSeriesMisterioIntrovertid@",
        "19HombreRockNatacionGamingAmbasThrillerIntrovertid@",
        "18MujerPopNinguno CineSeriesRomanticasIntrovertid@",
        "19MujerTodoGimnasioMusicaSeriesComediaExtrovertid@",
        "25MujerUrbanoFutbol Futbol AmbasAmorExtrovertid@",
        "18MujerTrapRugbyLa musica AmbasComediaExtrovertid@",
        "21MujerReggaetonVolleyballVideojuegosPeliculasSitcomsExtrovertid@",
        "24MujerPopNingunoIdiomas AmbasComedia Extrovertid@",
        "20MujerReggaeton NingunoTocar el saxofon AmbasTerrorIntrovertid@",
        "19MujerPunkAtletismoDibujarAmbasAnimeExtrovertid@",
        "25HombrePop BaseballEscuchar musicaAmbasSitcomsExtrovertid@",
        "21MujerReguetonFutbol EscribirAmbasAnimeIntrovertid@",
        "23MujerRapDeportes de montanaTocar guitarraPeliculasIntriga Extrovertid@",
        "24HombreIndie Atletismo DibujarAmbasComedia Introvertid@",
        "19HombreElectronica BaloncestoVer peliculas AmbasComedia Extrovertid@",
        "19HombreRapFutbolLeerSeriesAccion Extrovertid@",
        "20MujerPopVolleyballVideojuegosAmbasSuspenseExtrovertid@",
        "21HombreTodoGymCocinar AmbasAccion Introvertid@",
        "19HombreHip hopVolleyballEstar con mi familia AmbasRom-comsIntrovertid@",
        "19MujerFlamenco Futbol DibujarAmbasThrillerExtrovertid@",
    ]

    # Procesado de texto / Levistanche distance
    td0 = time.process_time_ns()
    dist2 = [
        distance.edit_distance(DataSetTFG[i], DataSetTFG[j])
        for i in range(1, len(DataSetTFG))
        for j in range(0, i)
    ]
    # Timepo distance
    tDistancia = time.process_time_ns() - td0
    # Configuración de cluster
    tc = time.process_time_ns()
    labels, error, nfound = PC.kmedoids(dist2, nclusters=5, npass=1000)
    cluster = dict()
    output = []
    w1 = csv.writer(open("ClusterTest.csv", "w"))
    for roommate, label in zip(DataSetTFG, labels):
        cluster.setdefault(label, []).append(roommate)
        w1.writerow([roommate, label])
    for label, grp in cluster.items():
        cluster_data = {}
        cluster_data["Roommate"] = grp
        cluster_data["label"] = str(label)
        output.append(cluster_data)
    tCluster = time.process_time_ns() - tc
    tIA = time.process_time_ns() - t0
    tClusterm = tCluster / 60000000000
    tDistanciam = tDistancia / 60000000000
    tIAm = tIA / 60000000000

    return jsonify(
        {"message": output},
        {"error": error},
        {"nfound": nfound},
        {"tiempoProcesado": tDistanciam},
        {"tiempoCluster": tClusterm},
        {"Tiempo IA": tIAm},
    )


# if __name__ == '__main__':
#     app.run(debug=True)