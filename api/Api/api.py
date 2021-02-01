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

# Import fake
from faker import Faker

faker = Faker()

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


# print(f'Name: {faker.name()}')
# print(f'First name: {faker.first_name()}')
# print(f'Last name: {faker.last_name()}')
# print(f'Male name: {faker.name_male()}')
# print(f'Female name: {faker.name_female()}')
# Mujeres 301 
#Hombres 186 - 5

@app.route("/api/fakeuserHomber", methods=["POST"])
def create_hombres():

    pasAll = "123";
    #Make hashed_pass = 
    with open('testH.json') as json_file:
        testS = json.load(json_file)
    for _ in range(186):
        name = faker.first_name_male()
        FlastName = faker.last_name()
        SlastName = faker.last_name()
        userName = name+"."+FlastName
        passx = name+pasAll;
        passHash = generate_password_hash(passx, method="sha256");

        new_user = User(
        public_id=str(uuid.uuid4()),
        userName=userName,
        password=passHash,
        admin=False)
        db.session.add(new_user)
        db.session.commit()
        new_resident = Residents(
            public_id=new_user.public_id,
            name=name,
            lastName=FlastName+ " "+ SlastName,
            sharedRoom=0,
            )
        db.session.add(new_resident)
        db.session.commit()
    count = 1
    users = User.query.all()
    for data in testS:
            new_test = TestR(
                public_id=users[count].public_id,
                gender=data["Sexo"],
                age=data["Edad"],
                musicGender=data["GustoMusical"],
                sport=data["Deporte"],
                hobbie=data["Hobbie"],
                movieSeries=data["Film"],
                filmGender=data["GeneroFilm"],
                tabaco=data["Tabaco"],
                alcohol=data["Alcohol"],
                party=data["Fiestas"],
                ordenConvivencia=data["OrdenLimpiezaDemas"],
                ordenPersonal=data["OrdenLimpiezaPersonal"],
                personalidad=data["personalidad"],
            )
            count += 1
            db.session.add(new_test)
            db.session.commit()     
        
        #print(f'Male name: {faker.first_name_male()}')
    
    return jsonify({"message": "New users created!"})

@app.route("/api/fakeuserMujeres", methods=["POST"])
def create_mujeres():

    pasAll = "123";
    #Make hashed_pass = 
    with open('testM.json') as json_file:
        testS = json.load(json_file)
    for _ in range(301):
        name = faker.first_name_female()
        FlastName = faker.last_name()
        SlastName = faker.last_name()
        userName = name+"."+FlastName
        passx = name+pasAll;
        passHash = generate_password_hash(passx, method="sha256");

        new_user = User(
        public_id=str(uuid.uuid4()),
        userName=userName,
        password=passHash,
        admin=False)
        db.session.add(new_user)
        db.session.commit()
        new_resident = Residents(
            public_id=new_user.public_id,
            name=name,
            lastName=FlastName+ " "+ SlastName,
            sharedRoom=0,
            )
        db.session.add(new_resident)
        db.session.commit()
    
    count = 188
    users = User.query.all()
    for data in testS:
            new_test = TestR(
                public_id=users[count].public_id,
                gender=data["Sexo"],
                age=data["Edad"],
                musicGender=data["GustoMusical"],
                sport=data["Deporte"],
                hobbie=data["Hobbie"],
                movieSeries=data["Film"],
                filmGender=data["GeneroFilm"],
                tabaco=data["Tabaco"],
                alcohol=data["Alcohol"],
                party=data["Fiestas"],
                ordenConvivencia=data["OrdenLimpiezaDemas"],
                ordenPersonal=data["OrdenLimpiezaPersonal"],
                personalidad=data["personalidad"],
            )
            count +=1
            db.session.add(new_test)
            db.session.commit()
        #print(f'Male name: {faker.first_name_male()}')
    
    return jsonify({"message": "New users created!"})

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
# Estructura
# {
#   "Edad" : 18,
#   "Sexo" : "Hombre",
#   "GustoMusical" : "Electronica",
#   "Deporte" : "Futbol",
#   "Hobbie" : "PlayStation",
#   "Film" : "Ambas",
#   "GeneroFilm" : "Accion",
#   "personalidad" : "Extrovertid@",
#   "Tabaco" : "No",
#   "Alcohol" : "No",
#   "Fiestas" : "Si",
#   "OrdenLimpiezaPersonal" : 8,
#   "OrdenLimpiezaDemas" : 8
# }

# 

# @app.route("/api/testHombreF", methods=["POST"])
# #@token_required
# def create_testF_hombres():
#     users = User.query.all()

#     with open('testM.json') as json_file:
#      testS = json.load(json_file)
#     count = 193
#     for data in testS:
#         new_test = TestR(
#             public_id=users[count].public_id,
#             gender=data["Sexo"],
#             age=data["Edad"],
#             musicGender=data["GustoMusical"],
#             sport=data["Deporte"],
#             hobbie=data["Hobbie"],
#             movieSeries=data["Film"],
#             filmGender=data["GeneroFilm"],
#             tabaco=data["Tabaco"],
#             alcohol=data["Alcohol"],
#             party=data["Fiestas"],
#             ordenConvivencia=data["OrdenLimpiezaDemas"],
#             ordenPersonal=data["OrdenLimpiezaPersonal"],
#             personalidad=data["personalidad"],
#         )
#         count += 1
#         db.session.add(new_test)
#         db.session.commit()

#     return jsonify({"message": "yes"})


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
            "-"
            +str(resident.id)
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

    labels, error, nfound = PC.kmedoids(distans, nclusters=5, npass=10)
    cluster = dict()
    output = []
    for roommate, label in zip(dataSet, labels):
        cluster.setdefault(label, []).append(roommate)
    for label, grp in cluster.items():
        cluster_data = {}
        cluster_data["Roommate"] = grp
        cluster_data["Count"] = len(grp)
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

    tests = TestR.query.filter_by(gender="Hombre").all()
    tiempoTI= time.process_time_ns()
    dataSet = []
    #Quitar asentos, ñ , etc..
    trans_tab = dict.fromkeys(map(ord, u"\u0301\u0308"), None)
    for test in tests:
        resident = Residents.query.filter_by(public_id=test.public_id).first()
        test_data = (
            "-"
            +str(resident.id)
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
            + " "+str(test.ordenConvivencia)
            + " "+str(test.ordenPersonal)
            + test.personalidad
        )
        test_data = normalize("NFKC", normalize("NFKD", test_data).translate(trans_tab))
        dataSet.append(test_data)

    tiempoPI= time.process_time_ns()
    distans = [
        distance.edit_distance(dataSet[i], dataSet[j])
        for i in range(1, len(dataSet))
        for j in range(0, i)
    ]
    tiempoPF= (time.process_time_ns() - tiempoPI)
    tiempoPF= tiempoPF /60000000000
    tiempoCI= time.process_time_ns()
    labels, error, nfound = PC.kmedoids(distans, nclusters=10, npass=10)
    cluster = dict()
    output = []
    for roommate, label in zip(dataSet, labels):
        cluster.setdefault(label, []).append(roommate)
    for label, grp in cluster.items():
        cluster_data = {}
        cluster_data["Roommate"] = grp
        cluster_data["Count"] = len(grp)
        cluster_data["label"] = str(label)
        output.append(cluster_data)
    tiempoCF= (time.process_time_ns()-tiempoCI)
    tiempoTF= (time.process_time_ns()-tiempoTI)
    tiempoCF= tiempoCF /60000000000
    tiempoTF= tiempoTF /60000000000


    #Asiganar a cuarto 
    # txt = "-1-18ElectronicaFutbolPlayStationAmbasAccionNoNoSi 8 8extro"
    # x = txt.split("-")
    # print(x[1])

    return jsonify({"testsHombres": output},
        {"error": error}, 
        {"nfound": nfound},
        {"TiempoTotal": tiempoTF},
        {"TiempoProcesado": tiempoPF},
        {"TiempoCluster": tiempoCF})

#Hacer los emparejamientos para mujeres

@app.route("/api/ia/matchsMujeres", methods=["GET"])
# @token_required
# def get_all_test(current_user):
def matchs_ia_mujeres():

    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    tests = TestR.query.filter_by(gender="Mujer").all()
    tiempoTI= time.process_time_ns()
    dataSet = []
    #Quitar asentos, ñ , etc..
    trans_tab = dict.fromkeys(map(ord, u"\u0301\u0308"), None)
    for test in tests:
        resident = Residents.query.filter_by(public_id=test.public_id).first()
        test_data = (
            "-"
            +str(resident.id)
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
            + " "+str(test.ordenConvivencia)
            + " "+str(test.ordenPersonal)
            + test.personalidad
        )
        test_data = normalize("NFKC", normalize("NFKD", test_data).translate(trans_tab))
        dataSet.append(test_data)
    tiempoPI= time.process_time_ns()
    distans = [
        distance.edit_distance(dataSet[i], dataSet[j])
        for i in range(1, len(dataSet))
        for j in range(0, i)
    ]
    tiempoPF= (time.process_time_ns() - tiempoPI)
    tiempoPF= tiempoPF /60000000000
    tiempoCI= time.process_time_ns()
    labels, error, nfound = PC.kmedoids(distans, nclusters=10, npass=10)
    cluster = dict()
    output = []
    for roommate, label in zip(dataSet, labels):
        cluster.setdefault(label, []).append(roommate)
    for label, grp in cluster.items():
        cluster_data = {}
        cluster_data["Roommate"] = grp
        cluster_data["Count"] = len(grp)
        cluster_data["label"] = str(label)
        output.append(cluster_data)

    tiempoCF= (time.process_time_ns()-tiempoCI)
    tiempoTF= (time.process_time_ns()-tiempoTI)
    tiempoCF= tiempoCF /60000000000
    tiempoTF= tiempoTF /60000000000
    return jsonify({"testsMujeres": output}, {"error": error}, {"nfound": nfound},{"TiempoTotal": tiempoTF},
        {"TiempoProcesado": tiempoPF},
        {"TiempoCluster": tiempoCF})



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




@app.route("/api/ia/matchsHombresT", methods=["GET"])
# @token_required
# def get_all_test(current_user):
def matchs_ia_hombresTest():

    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    tests = TestR.query.filter_by(gender="Hombre").all()
    tiempoTI= time.process_time_ns()
    dataSet = []
    #Quitar asentos, ñ , etc..
    trans_tab = dict.fromkeys(map(ord, u"\u0301\u0308"), None)
    for test in tests:
        resident = Residents.query.filter_by(public_id=test.public_id).first()
        test_data = (
            "-"
            +str(resident.id)
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
            + " "+str(test.ordenConvivencia)
            + " "+str(test.ordenPersonal)
            + test.personalidad
        )
        test_data = normalize("NFKC", normalize("NFKD", test_data).translate(trans_tab))
        dataSet.append(test_data)

    tiempoPI= time.process_time_ns()
    distans = [
        distance.edit_distance(dataSet[i], dataSet[j])
        for i in range(1, len(dataSet))
        for j in range(0, i)
    ]
    tiempoPF= (time.process_time_ns() - tiempoPI)
    tiempoPF= tiempoPF /60000000000
    tiempoCI= time.process_time_ns()
    labels, error, nfound = PC.kmedoids(distans, nclusters=10, npass=10)
    cluster = dict()
    output = []
    outputId = []
    for roommate, label in zip(dataSet, labels):
        cluster.setdefault(label, []).append(roommate)
    for label, grp in cluster.items():
        cluster_data = {}
        cluster_dataID = {}
        cluster_data["Roommate"] = grp
        cluster_dataID["resultados"] = grp
        cluster_data["Count"] = len(grp)
        cluster_data["label"] = str(label)
        output.append(cluster_data)
        outputId.append(cluster_dataID)
    tiempoCF= (time.process_time_ns()-tiempoCI)
    tiempoTF= (time.process_time_ns()-tiempoTI)
    tiempoCF= tiempoCF /60000000000
    tiempoTF= tiempoTF /60000000000
    
    # for cluster in output:

    # new_room = Rooms(state="Ocupado")
    # db.session.add(new_room)
    # db.session.commit()

    # new_match = Matches(user_id=resident.public_id, room_id=room.id)
    # db.session.add(new_match)
    # db.session.commit()



    #Asiganar a cuarto 
     txt = "-1-18ElectronicaFutbolPlayStationAmbasAccionNoNoSi 8 8extro"
     x = txt.split("-")
     print(x[1])

    return jsonify({"testsHombres": outputId})


# if __name__ == '__main__':
#     app.run(debug=True)