from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    token = db.Column(db.String(120), unique=False, nullable=True)

    @staticmethod
    def get_with_login_credentials(email, password):
        return User.query.filter_by(email=email).filter_by(password=password).first()

    # como primer parametro se pasa self, pero a la hora de llamar la funcion no se pone
    def assign_token(self,token):
        self.token = token
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_with_token(token):
        return User.query.filter_by(token=token).first()

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__="Planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    population = db.Column(db.String(120), unique=False, nullable=False)
    terrain = db.Column(db.String(120), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain
        }

        
class People(db.Model):
    __tablename__="People"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    eye_color = db.Column(db.String(25), unique=False, nullable=False)
    gender = db.Column(db.String(25), unique=False, nullable=False)
    hair_color = db.Column(db.String(25), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            # do not serialize the password, its a security breach
        }
    
    def db_post(self):        
        db.session.add(self)
        db.session.commit()


    def put_with_json(self,json):
        if json["name"]:
            self.name = json["name"]
        if json["eye_color"]:
            self.eye_color = json["eye_color"]
     

    def set_with_json(self,json):
        self.name = json["name"]
        self.eye_color = json["eye_color"]
        self.hair_color = json["hair_color"]
        self.gender = json["gender"]

