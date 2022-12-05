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
from app.models import Box, Indication
from app import db

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
	
	box = Box.query.filter_by(name = data['name']).first()
	if box is not None:
		ind = Indication(onBox=box, temp = data['temp'], hum=data['hum'], 
				  time = datetime.now())
		db.session.add(ind)
		db.session.commit()
		return "OK"
	else:
		return "404"
		
@app.route('/api/get', methods=['GET'])
def get():
	inds = Indication.query.all()
	strin = ""
	for ind in inds:
		strin+=str(ind.temp) + " " + str(ind.hum) + " " + str(ind.onBox.name) + "\n" + "|"
	return strin

	
	

