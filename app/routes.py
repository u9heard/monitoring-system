from app import app
from flask import render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from flask_login import login_required
from werkzeug.urls import url_parse
from flask import request
from datetime import datetime
from datetime import timedelta
from app.models import Box, Indication
from app import db
from flask import jsonify
from sqlalchemy.sql.expression import func



@app.route('/')
@app.route('/index')
@login_required
def index():
	user = {'username': 'Ilya'}
	return render_template('index.html', title='Home', user = user)
	
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/api/add', methods=['POST'])
def add_to_db():
	data = request.get_json()
	
	box = Box.query.filter_by(id_device = data['id']).first()
	if box is not None:
		ind = Indication(onBox=box, temp = data['temp'], hum=data['hum'], 
				  time = datetime.now())
		db.session.add(ind)
		db.session.commit()
		
		return "OK"
	else:
		return "404"
		
@app.route('/api/get', methods=['GET'])
@login_required
def get_all():
	indications = Indication.query.all()
	data = {}
	indata = []
	
	for ind in indications:
		indata.append({
			"id": ind.onBox.id,
			"temp": ind.temp,
			"hum": ind.hum,
			"date": ind.time.strftime("%Y-%m-%dT%H:%M:%S")
		})
	
	data["data"] = indata
	# for ind in inds:
	# 	strin+=str(ind.temp) + " " + str(ind.hum) + " " + str(ind.onBox.name) + "\n" + "|"
	return jsonify(data)

@app.route('/api/get/<string:id>', methods=['GET'])
@login_required
def get_box(id):
	bx = Box.query.where(Box.name==id).first()
	#indications = Indication.query.where(Indication.id_box==bx.id)
	indications = Indication.query.where(Indication.id_box==bx.id).filter(Indication.time > datetime.now()-timedelta(hours=24))

	
	data = {}
	indata = []
	
	for ind in indications:
		indata.append({
			"id": ind.onBox.id,
			"temp": ind.temp,
			"hum": ind.hum,
			"date": ind.time.strftime("%Y-%m-%dT%H:%M:%S")
		})
	
	data["data"] = indata
	# for ind in inds:
	# 	strin+=str(ind.temp) + " " + str(ind.hum) + " " + str(ind.onBox.name) + "\n" + "|"
	return jsonify(data)

@app.route('/api/get/last')
@login_required
def get_last_all():
	inds = db.session.query(Indication.id_box, 
	Indication.temp, Indication.hum,
	func.max(Indication.time).label("time")).group_by(Indication.id_box)

	data = []

	for i in inds:
		data.append({
			"id_box": i.id_box,
			"temp": i.temp,
			"hum": i.hum,
			"time": i.time.strftime("%Y-%m-%dT%H:%M:%S")
		})
	return jsonify(data)


@app.route('/dashboard')
@login_required
def dashboards():
	inds = db.session.query(Indication.id_box, 
	Indication.temp, Indication.hum,
	func.max(Indication.time).label("time")).group_by(Indication.id_box)

	# for i in inds:
	# 	data.append({
	# 		"id_box": i.id_box,
	# 		"temp": i.temp,
	# 		"hum": i.hum,
	# 		"time": i.time.strftime("%Y-%m-%dT%H:%M:%S")
	# 	})
	return render_template('dash_def.html', objects = inds)

@app.route('/dashboards')
@login_required
def dashboard():
	return render_template('dashboard.html')

@app.route('/last_data')
def last_data():
	return "Hehehe"
	