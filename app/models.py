from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
		
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
		
	

	def __repr__(self): #Сообщает ка кпечатать этот объект
		return '<User {}>'.format(self.username)
		
	@login.user_loader
	def load_user(id):
		return User.query.get(int(id))
		
class Box(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	Indications = db.relationship('Indication', backref='onBox', lazy='dynamic')
	
	def __repr__(self): #Сообщает ка кпечатать этот объект
		return '<Box {}>'.format(self.name)
		
class Indication(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_box = db.Column(db.Integer, db.ForeignKey('box.id'))
	temp = db.Column(db.Float)
	hum = db.Column(db.Float)
	time = db.Column(db.DateTime)
	
	def __repr__(self): #Сообщает ка кпечатать этот объект
		return '<Temp: {0}; Hum: {1}, DT: {2}>'.format(self.temp, self.hum, self.time.strftime("%m/%d/%Y, %H:%M:%S"))
		
		
class Device(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	
