from flask_login import login_required
from app.api import bp
from app.api.auth import token_auth
from app.models import Indication
from app.models import Box
from app.api.errors import bad_request
from flask import jsonify, request, g
from datetime import datetime, timedelta
from app import app, db
from sqlalchemy import func


@bp.route('/indications/add', methods=['POST'])
# @token_auth.login_required
def add_ind():
    data = request.get_json()
	
    box = Box.query.get(data['id'])
    if box is not None:
        ind = Indication(onBox=box, temp = data['temp'], hum=data['hum'], 
                    time = datetime.now())
        db.session.add(ind)
        db.session.commit()
        
        return "OK"
    else:
        return "not ok"
    

@app.route('/indications/last')
@login_required
def get_online_web():
    return get_online()

@bp.route('/indications/last')
@token_auth.login_required
def get_online_api():
    return get_online()

@app.route('/indications/<string:id>', methods=['GET'])
#@login_required
def get_inds_web(id):
    return get_inds(id)


@bp.route('/indications/<string:id>', methods=['GET'])
@token_auth.login_required
def get_inds_api(id):
    
    return get_inds(id)


def get_inds(id):

    bx = Box.query.where(Box.name==id).first()
	#indications = Indication.query.where(Indication.id_box==bx.id)
    start_time = request.args.get('start')
    end_time = request.args.get('end')


    if start_time is not None and end_time is not None:
        indications = Indication.query.where(Indication.id_box==bx.id).filter(Indication.time > datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S"), Indication.time < datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S"), Indication.time < datetime.now())
    else:
        indications = Indication.query.where(Indication.id_box==bx.id).filter(Indication.time > datetime.now()-timedelta(hours=1), Indication.time < datetime.now())


    data = {}
    indata = []
    i=0
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


def get_online():
    inds = db.session.query(Indication.id_box, Box.name,
		Indication.temp, Indication.hum,
		func.max(Indication.time).label("time")).join(Box, Indication.id_box==Box.id).group_by(Indication.id_box).filter(Indication.time > datetime.now()-timedelta(hours=24))

    if not inds:
        return []

    data = []

    for i in inds:
        data.append({
            "id_box": i.id_box,
            "name": i.name,
            "temp": i.temp,
            "hum": i.hum,
            "time": i.time.strftime("%Y-%m-%dT%H:%M:%S")
        })
    return jsonify(data)