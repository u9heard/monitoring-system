from app import app
from flask import render_template, flash, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app.forms import LoginForm, DataForm, FileForm, ConfigForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Device
from flask_login import login_required
from werkzeug.urls import url_parse
from flask import request
from datetime import datetime
from datetime import timedelta
from app.models import Box, Indication, Log
from app import db
from flask import jsonify, send_file
from sqlalchemy.sql.expression import func
from os import path
import os
from werkzeug.utils import secure_filename
import json
from decimal import Decimal
from app import login

from app import notifications



@app.route('/')
@app.route('/index')
@login_required
def index():
	log = Log.query.order_by(Log.id)

	return render_template('index.html', title='Home', log=log)
	
	
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
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

		
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

# @app.route('/get/<string:id>', methods=['GET'])
# @login_required
# def get_box(id):
# 	bx = Box.query.where(Box.name==id).first()
# 	#indications = Indication.query.where(Indication.id_box==bx.id)
# 	start_time = request.args.get('start')
# 	end_time = request.args.get('end')
	
	
# 	if start_time is not None and end_time is not None:
# 		indications = Indication.query.where(Indication.id_box==bx.id).filter(Indication.time > datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S"), Indication.time < datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S"), Indication.time < datetime.now())
# 	else:
# 		indications = Indication.query.where(Indication.id_box==bx.id).filter(Indication.time > datetime.now()-timedelta(hours=1), Indication.time < datetime.now())

	
# 	data = {}
# 	indata = []
# 	i=0
# 	for ind in indications:
# 		if i%5==0:

# 			indata.append({
# 				"id": ind.onBox.id,
# 				"temp": ind.temp,
# 				"hum": ind.hum,
# 				"date": ind.time.strftime("%Y-%m-%dT%H:%M:%S")
# 			})
# 		i+=1
	
# 	data["data"] = indata
# 	# for ind in inds:
# 	# 	strin+=str(ind.temp) + " " + str(ind.hum) + " " + str(ind.onBox.name) + "\n" + "|"
# 	return jsonify(data)

# @app.route('/api/get/last') #replaced
# @login_required
# def get_last_all():
# 	inds = db.session.query(Indication.id_box, Box.name,
# 		Indication.temp, Indication.hum,
# 		func.max(Indication.time).label("time")).join(Box, Indication.id_box==Box.id).group_by(Indication.id_box).filter(Indication.time > datetime.now()-timedelta(hours=24))

# 	if not inds:
# 		return []

# 	data = []

# 	for i in inds:
# 		data.append({
# 			"id_box": i.id_box,
# 			"name": i.name,
# 			"temp": i.temp,
# 			"hum": i.hum,
# 			"time": i.time.strftime("%Y-%m-%dT%H:%M:%S")
# 		})
# 	return jsonify(data)


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


@app.route('/logs')
@login_required
def logs():
	log_list = Log.query.all()
	
	data = []
	for l in log_list:
		data.append({
			"num": l.id,
			"name": l.name,
			"path": l.path,
			"time": l.date
		})

	return jsonify(data)

# @app.route('/logs/<path:filename>')
# def download_log(filename):
# 	return "Hello"

@app.route('/logs/create', methods=['GET', 'POST'])
@login_required
def create_log():
	form = DataForm()
	
	form.box_field.choices = [(b.id, b.name) for b in Box.query.order_by(Box.id).all()]
	if form.validate_on_submit():
		bx = Box.query.filter_by(id=form.box_field.data).first()
		
		indications = Indication.query.where(Indication.id_box==bx.id).filter(Indication.time > form.date_start.data, Indication.time < form.date_end.data).order_by(Indication.time)

		data=[]

		for i in indications:
			data.append({
				"id_box": i.id_box,
				"temp": i.temp,
				"hum": i.hum,
				"time": i.time.strftime("%Y-%m-%dT%H:%M:%S")
		})
		with open('logs/{0}-{1}-{2}.json'.format(bx.name, datetime.strftime(form.date_start.data, "%Y-%m-%dT%H:%M:%S"), datetime.strftime(form.date_end.data, "%Y-%m-%dT%H:%M:%S")), 'w') as file:
			file.write(json.dumps(data))
			log = Log(name=bx.name, date='{0}-{1}'.format(form.date_start.data, form.date_end.data), path='logs/{0}-{1}-{2}.json'.format(bx.name, datetime.strftime(form.date_start.data, "%Y-%m-%dT%H:%M:%S"), datetime.strftime(form.date_end.data, "%Y-%m-%dT%H:%M:%S")))
			db.session.add(log)
			db.session.commit()
		return redirect(url_for('index'))
		
	return render_template('create.html', form=form)

# @app.route('/upload', methods=['GET', 'POST'])
# @login_required
# def upload():
# 	form = FileForm()

# 	if form.validate_on_submit():
# 		filename = secure_filename(form.file.data.filename)
# 		form.file.data.save('uploads/'+filename)

# 		name = filename.partition('-')[0]

# 		with open('uploads/'+filename) as f:
# 			data = json.load(f)
# 			bx = Box.query.filter_by(name=name).first()
			
# 			for dt in data['list']:
				
# 				ind = Indication(onBox=bx, temp=round(dt['temperature']*1.8+32, 1),
# 		     			hum=dt['humidity'], time=datetime.strptime(dt['time'], "%Y-%m-%dT%H:%M:%S"))
# 				db.session.add(ind)
			
# 			db.session.commit()
				

# 		return redirect(url_for('index'))
# 	return render_template('upload.html', form = form)

@app.route('/logs/<path:filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
	
	return send_file('/var/www/foodrus/logs/'+filename, as_attachment=True)

@app.route('/delete/<path:filename>', methods=['GET', 'POST'])
@login_required
def delete(filename):
	f = str(filename).partition('/')[2]
	
	l = Log.query.filter_by(path='logs/'+f).first()
	print(l.name)

	db.session.delete(l)
	db.session.commit()

	return redirect(url_for('index'))


# @app.route('/webdash/<string:id>', methods=['GET', 'POST'])
# def webdash(id):
# 	return render_template("graphview.html", jid=id)

@app.route('/firebase-messaging-sw.js', methods=['GET', 'POST'])
@login_required
def firebase():
	return send_from_directory('static/js/', 'firebase-messaging-sw.js')


# @app.route('/config', methods=['GET', 'POST'])
# def configuration():
# 	devices = db.session.query(Box.id, Device.address, Box.name).join(Device, Device.id == Box.id_device, isouter = True) 

# 	dev_list = ['Не заменять', 'None']
# 	[dev_list.append(d.address) for d in Device.query.all()]
	

# 	return render_template('config.html', devices=devices, dev_list=dev_list)


@app.route('/notify', methods=['GET', 'POST'])
@login_required
def notify():
	
	#notifications.send_notifications_to_all('test_title', 'test_text')
	return notifications.send_to_all('test_title', 'test_text')
