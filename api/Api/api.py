from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
 


app.config['SECRET_KEY'] = 'FuckTheRandomness'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://douglas:douglas98@localhost/tfgTest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Models
#Table Users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    userName = db.Column(db.String(20))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

#Table testResidents
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
    personalidad = db.Column(db.String(10)) #Introver - Extro  

#Table Residentes
class Residents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50))
    name = db.Column(db.String(30))
    lastName = db.Column(db.String(50))
    sharedRoom = db.Column(db.Boolean)

#Table Habitaciones

class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20))

#Table emparejamientos

class Matches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer) 
    room_id = db.Column(db.Integer)



#Api resources    
#Token verification
#Ningun usuario podra acceder a los endpoints sin un token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


     
#EndPoints      
#Get todos los usuarios
@app.route('/api/user', methods=['GET'])
@token_required
def get_all_users(current_user):

   if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

   users = User.query.all()

   output = []

   for user in users:
      user_data = {}
      user_data['user_id'] = user.id
      user_data['public_id'] = user.public_id
      user_data['userName'] = user.userName
      user_data['password '] = user.password
      user_data['admin'] = user.admin
      output.append(user_data)

   return jsonify({'users' : output})

#Get all residentes
@app.route('/api/residents', methods=['GET'])
@token_required
def get_all_residents(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot performs that funtion!'})
    
    residents = Residents.query.all()

    output = []

    for resident in residents:

        resident_data = {}
        resident_data['resident_Id'] = resident.id
        resident_data['public_Id'] = resident.public_id
        resident_data['name'] = resident.name
        resident_data['lastName'] = resident.lastName
        resident_data['sharedRoom'] = resident.sharedRoom
        output.append(resident_data)
    
    return jsonify({'residents' : output})

#Get one resident info from resident by public id
@app.route('/api/resident/<public_id>', methods=['GET'])
@token_required
def get_resident(current_user,public_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot performs that funtion!'})
    
    resident = Residents.query.filter_by(public_id=public_id).first()
    if not resident:
        return jsonify({'message' : 'Dude, no resident found ! :('}),404

    resident_data = {}
    resident_data['name'] = resident.name
    resident_data['lastName'] = resident.lastName
    resident_data['sharedRoom'] = resident.sharedRoom
    return jsonify({'resident' : resident_data})


#get user/public_id usuario especifico
@app.route('/api/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user,public_id):

   user = User.query.filter_by(public_id=public_id).first()

   if not user :
      return jsonify({'message': 'Dude, no user found ! :('})
   
   user_data = {}
   user_data['public_id'] = user.public_id
   user_data['userName'] = user.userName
   user_data['password '] = user.password
   user_data['admin'] = user.admin
   return jsonify({'user' : user_data})




#Create new user
@app.route('/api/user', methods=['POST'])
#@token_required
def create_user():
   data = request.get_json()
   hashed_password = generate_password_hash(data['password'], method='sha256')

   new_user = User(public_id=str(uuid.uuid4()), userName=data['userName'], password=hashed_password, admin=False)
   db.session.add(new_user)
   db.session.commit()

   return jsonify({'message' : 'New user created!'})

#Create residente ( public_id = user.public_id, name, lastName, sharedRoom (True or false))
# json { "name": "name", "lastName": "lastname", "sharedRoom": "1/0"}
@app.route('/api/residente/<public_id>', methods=['POST'])
@token_required
def create_resident(current_user,public_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()
    user = User.query.filter_by(public_id=public_id).first()

    if not user :
      return jsonify({'message': 'Dude, no user found ! :('}),404

    new_resident = Residents(   public_id=public_id, 
                                name =data['name'],
                                lastName=data['lastName'],
                                sharedRoom=data['sharedRoom'])
    
    db.session.add(new_resident)
    db.session.commit()

    return jsonify({'message' : 'New resident created!'}),200


#Promover usuario a admin , solo un admin puede hacer eso
@app.route('/api/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user,public_id):

   user = User.query.filter_by(public_id=public_id).first()

   if not user :
      return jsonify({'message': 'Dude, no user found ! :('})
   
   user.admin = True
   db.session.commit()
   return jsonify({'message' : 'user has been promoted!'})


#borrar un usuario, solo un admin podra
@app.route('/api/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user,public_id):

   if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

   user = User.query.filter_by(public_id=public_id).first()

   if not user:
      return jsonify({'message' : 'No user found!'})

   db.session.delete(user)
   db.session.commit()

   return jsonify({'message' : 'The user has been deleted!'})


#Login , comprueba credenciales, genera token el cual se necesita para acceder a los endpoints
@app.route('/api/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Falta Data', 401)

    user = User.query.filter_by(userName=auth.username).first()

    if not user:
        return make_response('Could not verify', 401)

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401)


#ver perfil
@app.route('/api/perfil', methods=['GET'])
@token_required
def ver_perfil(current_user):

    #Object residente
    resident = Residents.query.filter_by(public_id=current_user.public_id).first()
    #Room, se tendra que ir a room buscar el id del usuario
    
    resident_data = {}
    resident_data['name'] = resident.name
    resident_data['lastName'] = resident.lastName
    resident_data['sharedRoom'] = resident.sharedRoom
    return jsonify({'resident' : resident_data})
        

#EndPoint test
#Hacer test, crea el test en base al currente user osea que el usuario que llame al endpoint de test guardara eso
@app.route('/api/test', methods=['POST'])
@token_required
def create_test(current_user):
   
   data = request.get_json()

#    {
#     "gender":"Hombre", string
#     "age" : 22,  int
#     "musicGender" : "EDM", string
#     "sport" : "Volleyball", string
#     "hobbie" : "Videojuegos", string
#     "movieSeries" : "Peliculas", string
#     "filmGender" : " Thriller", string
#     "tabaco": "no",  si/no
#     "alcohol": "si", si/no
#     "party" : "si", si/no
#     "ordenConvivencia" : 7 , int
#     "ordenPersonal" : 5, int
#     "personalidad" : "intro" , intro o extro  
# }
 
   new_test = TestR(public_id=current_user.public_id,
                     gender=data['gender'],
                     age=data['age'],
                     musicGender=data['musicGender'],
                     sport = data['sport'],
                     hobbie = data['hobbie'],
                     movieSeries = data['movieSeries'],
                     filmGender = data['filmGender'],
                     tabaco = data['tabaco'],
                     alcohol = data['alcohol'],
                     party = data['party'],
                     ordenConvivencia = data['ordenConvivencia'],
                     ordenPersonal = data['ordenPersonal'],
                     personalidad = data['personalidad'])
   db.session.add(new_test)
   db.session.commit()

   return jsonify({'message' : "Test created!!!"})

#obtener un test de usuario especifico
@app.route('/api/test/<public_id>', methods=['GET'])
@token_required
def get_one_test(current_user,public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user :
      return jsonify({'message': 'Dude, no user found ! :('})

    test = TestR.query.filter_by(user_id=user.public_id).first()

    if not test :
      return jsonify({'message': 'Dude, no test available ! :('})
    
    test_data = {}

    test_data['gender'] = test.gender
    test_data['age'] = test.age
    test_data['musicGender'] = test.musicGender
    test_data['sport'] = test.sport
    test_data['hobbie'] = test.hobbie
    test_data['movieSeries'] = test.movieSeries
    test_data['filmGender'] = test.filmGender
    test_data['tabaco'] = test.tabaco
    test_data['alcohol'] = test.alcohol
    test_data['party'] = test.party
    test_data['ordenConvivencia'] = test.ordenConvivencia
    test_data['ordenPersonal'] = test.ordenPersonal
    test_data['personalidad'] = test.personalidad
    return jsonify({'test' : test_data})


#get all test avaible

@app.route('/api/allTest', methods=['GET'])
@token_required
def get_all_test(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    tests = TestR.query.all()

    output = []

    for test in tests:
        test_data = {}
        test_data['user_id'] = test.public_id
        test_data['gender'] = test.gender
        test_data['age'] = test.age
        test_data['musicGender'] = test.musicGender
        test_data['sport'] = test.sport
        test_data['hobbie'] = test.hobbie
        test_data['movieSeries'] = test.movieSeries
        test_data['filmGender'] = test.filmGender
        test_data['tabaco'] = test.tabaco
        test_data['alcohol'] = test.alcohol
        test_data['party'] = test.party
        test_data['ordenConvivencia'] = test.ordenConvivencia
        test_data['ordenPersonal'] = test.ordenPersonal
        test_data['personalidad'] = test.personalidad
        output.append(test_data)
    
    return jsonify({'tests' : output})

#get all test  hombre 

@app.route('/api/test/Hombre', methods=['GET'])
@token_required
def get_all_test_men(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    tests = TestR.query.filter_by(gender = "masculino").all()

    output = []

    for test in tests:
        test_data = {}
        test_data['user_id'] = test.public_id
        test_data['gender'] = test.gender
        test_data['age'] = test.age
        test_data['musicGender'] = test.musicGender
        test_data['sport'] = test.sport
        test_data['hobbie'] = test.hobbie
        test_data['movieSeries'] = test.movieSeries
        test_data['filmGender'] = test.filmGender
        test_data['tabaco'] = test.tabaco
        test_data['alcohol'] = test.alcohol
        test_data['party'] = test.party
        test_data['ordenConvivencia'] = test.ordenConvivencia
        test_data['ordenPersonal'] = test.ordenPersonal
        test_data['personalidad'] = test.personalidad
        output.append(test_data)
    
    return jsonify({'tests' : output})

#get all test  Mujer
@app.route('/api/test/Mujer', methods=['GET'])
@token_required
def get_all_test_female(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    tests = TestR.query.filter_by(gender = "femenino").all()

    output = []

    for test in tests:
        test_data = {}
        test_data['user_id'] = test.public_id
        test_data['gender'] = test.gender
        test_data['age'] = test.age
        test_data['musicGender'] = test.musicGender
        test_data['sport'] = test.sport
        test_data['hobbie'] = test.hobbie
        test_data['movieSeries'] = test.movieSeries
        test_data['filmGender'] = test.filmGender
        test_data['tabaco'] = test.tabaco
        test_data['alcohol'] = test.alcohol
        test_data['party'] = test.party
        test_data['ordenConvivencia'] = test.ordenConvivencia
        test_data['ordenPersonal'] = test.ordenPersonal
        test_data['personalidad'] = test.personalidad
        output.append(test_data)
    
    return jsonify({'tests' : output})


#make a room
@app.route('/api/room', methods=['POST'])
@token_required
def create_room(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    data = request.get_json()

    new_room = Rooms(state = data['state'])

    db.session.add(new_room)
    db.session.commit()

    return jsonify({'message' : 'New room created !'})


#update state of room

@app.route('/api/room/<room_id>', methods=['PUT'])
@token_required
def update_state_room(current_user,room_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}),401
    
    room = Rooms.query.filter_by(id = room_id).first()

    if not room:
        return jsonify({'message' : 'No room found!'})
    
    data = request.get_json()

    room.state = data['state']
    db.session.commit()

    return jsonify({'message' : ' Rooms state update :D!'})
    
#End point Get resultados de una habitación table rooms
@app.route('/api/room/<room_id>', methods=['GET'])
@token_required
def get_room_residents(current_user,room_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}),401

    room = Rooms.query.filter_by(id = room_id).first()

    if not room:
        return jsonify({'message' : 'No room found!'})
    
    room_data = {}
    room_data['roomID'] = room.id
    room_data['State'] = room.state

    return jsonify({'Room': room_data})

#End point get all rooms from rooms table
@app.route('/api/room', methods=['GET'])
@token_required
def get_all_rooms(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}),401

    rooms = Rooms.query.all()

    output = []

    for room in rooms:
        room_data = {}
        room_data['roomID'] = room.id
        room_data['State'] = room.state
        output.append(room_data)
    
    return jsonify({ 'rooms': output})


#agregar resident a una habitación o asociar una habitación a un resident
#post
# class Matches(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer) 
#     room_id = db.Column(db.Integer)

@app.route('/api/match/<room_id>/<public_id>', methods=['POST'])
@token_required
def add_room_to_resident(current_user,room_id,public_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    room = Rooms.query.filter_by(id = room_id).first()
    
    
    if not room:
        return jsonify({'message' : 'No room found!'}), 404
    
    resident = Residents.query.filter_by(public_id=public_id).first()
    if not resident:
        return jsonify({'message' : 'Dude, no resident found ! :('}),404

    new_match = Matches( user_id=resident.public_id, room_id= room.id)
    db.session.add(new_match)
    db.session.commit()

    return jsonify({'message' : 'New match add!'})



#End point dar los resultados en tabla matchets con id room
@app.route('/api/match/<room_id>', methods=['GET'])
@token_required
def get_matchs_room(current_user,room_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}),401

    room = Rooms.query.filter_by(id = room_id).first()
    
    if not room:
        return jsonify({'message' : 'Dude, no room found'}), 404

    matchR = Matches.query.filter_by(room_id= room.id).first()
    if not matchR:
        return jsonify({'message' : 'Dude, no room in matchs table'}), 404
    
    
    matchAll = Matches.query.filter_by(room_id = room.id).all()
    
    output = []

    for match in matchAll:
        match_data = {}
        resident = Residents.query.filter_by(public_id=match.user_id).first()
        match_data['room_id'] = match.room_id
        match_data['Resident Name'] = resident.name
        output.append(match_data)
    
    return jsonify({'matches' : output})

#get your personal result with your token xd
@app.route('/api/result', methods=['GET'])
@token_required
def get_result(current_user):
    

    resident = Residents.query.filter_by(public_id = current_user.public_id).first()
    
    if not resident:
        return jsonify({'message' : 'Dude, no resident found'}), 404

    matchR = Matches.query.filter_by(user_id= resident.public_id).first()
    if not matchR:
        return jsonify({'message' : ' Not result in match :('}), 404
    
    
    matchAll = Matches.query.filter_by(room_id = matchR.room_id).all()
    
    output = []

    for match in matchAll:
        match_data = {}
        resident = Residents.query.filter_by(public_id=match.user_id).first()
        match_data['room_id'] = match.room_id
        match_data['user_id'] = match.user_id
        match_data['Resident Name'] = resident.name
        output.append(match_data)
    
    return jsonify({'matches' : output})












# if __name__ == '__main__':
#     app.run(debug=True)