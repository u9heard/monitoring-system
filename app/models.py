from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime, timedelta
import base64
import os

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	token = db.Column(db.String(32),index=True, unique=True)
	token_expiration = db.Column(db.DateTime)

	fcmtoken = db.Column(db.String(256))
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
		
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
		
	def set_fcm(self, token):
		self.fcmtoken = token
	
	def get_fcm(self):
		return self.fcmtoken
	
	#TOKENS
	def get_token(self, expires_in=3600):
		now = datetime.now()

		if self.token and self.token_expiration > now+timedelta(seconds=60):
			return self.token
		self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
		self.token_expiration = now + timedelta(seconds=expires_in)
		db.session.add(self)
		return self.token
	
	def revoke_token(self):
		self.token_expiration = datetime.now() - timedelta(seconds=1)

	@staticmethod
	def check_token(token):
		user = User.query.filter_by(token=token).first()
		if user is None or user.token_expiration < datetime.now():
			return None
		return user



	def __repr__(self): #Сообщает ка кпечатать этот объект
		return '<User {}>'.format(self.username)
		
	@login.user_loader
	def load_user(id):
		return User.query.get(int(id))
	
	def to_dict(self):
		data = {
			"id": self.id,
			"username": self.username,
			"email": self.email,

		}
		return data
		
class Box(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	Indications = db.relationship('Indication', backref='onBox', lazy='dynamic')
	id_device = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=True, unique=True)
	
	def __repr__(self): #Сообщает ка кпечатать этот объект
		return '<Box {}>'.format(self.name)
		

class Indication(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_box = db.Column(db.Integer, db.ForeignKey('box.id'))
	temp = db.Column(db.Float)
	hum = db.Column(db.Float)
	time = db.Column(db.DateTime)
	
	def to_dict(self):
		data = {
			'id' : self.id,
			'id_box' : self.id_box,
			'temp' : self.temp,
			'hum' : self.hum,
			'time' : self.time
		}

		return data

	def __repr__(self): #Сообщает ка кпечатать этот объект
		return '<Temp: {0}; Hum: {1}, DT: {2}>'.format(self.temp, self.hum, self.time.strftime("%m/%d/%Y, %H:%M:%S"))
	
	@staticmethod
	def to_collection_dict(query):
		data = {
			"data" : [item.to_dict() for item in query]
		}
		return data
		
		
class Device(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	address = db.Column(db.String(64))
	Boxes = db.relationship('Box', backref='onDevice', uselist=False)
	
	def __repr__(self):
		return '<Device: {0}>'.format(self.address, self.Boxes)
	
	
class Log(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64))
	date = db.Column(db.String(64))
	path = db.Column(db.String(64))

	def __repr__(self):
		return '<Log: {0} {1} {2} {3}>'.format(self.name, self.id, self.date, self.path)
	