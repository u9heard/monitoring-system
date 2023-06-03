from flask_login import login_required
from app.api import bp
from app.api.auth import token_auth, login_or_token_required
from app.models import Indication, Box, Device, Alert
from app.api.errors import bad_request
from flask import jsonify, request, g
from datetime import datetime, timedelta
from app import app, db
from sqlalchemy import func, desc
from app import notifications


@bp.route('/indications/add', methods=['POST'])
def add_to_db():
    data = request.get_json()

    

    device_from = Device.query.where(Device.address == data["addr"]).first()

    if device_from is None:
        new_device = Device(address=data["addr"])
        db.session.add(new_device)
        db.session.commit()

        empty_box = Box.query.where(Box.onDevice == None).first() 
        empty_box.id_device = new_device.id 
        db.session.commit()

        new_ind = Indication(onBox=empty_box, temp=data["temp"], hum=data["hum"])
        db.session.add(new_ind)
        db.session.commit()
    else:
        box = Box.query.where(Box.id_device == device_from.id).first()

        if box.box_active == 0:
            return "OK"

        current_date = datetime.now()
        if box.alert_active == 1:
            last_alert = Alert.query.where(Alert.id_box == box.id).order_by(desc(Alert.date)).first()
            if last_alert is None:
                checked_alert_temp = check_temp(box, data["temp"], current_date)
                checked_alert_hum = check_hum(box, data["hum"], current_date)
                if checked_alert_temp is not None:
                    db.session.add(checked_alert_temp)
                if checked_alert_hum is not None:
                    db.session.add(checked_alert_hum)
            elif last_alert.date < current_date-timedelta(minutes=5):
                checked_alert_temp = check_temp(box, data["temp"], current_date)
                checked_alert_hum = check_hum(box, data["hum"], current_date)
                if checked_alert_temp is not None:
                    db.session.add(checked_alert_temp)
                if checked_alert_hum is not None:
                    db.session.add(checked_alert_hum)
                
                
        new_ind = Indication(onBox=box, temp=float(data["temp"])+device_from.correct_t, hum=float(data["hum"])+device_from.correct_h, time=current_date) #TODO: check this
        db.session.add(new_ind)
        db.session.commit()

    return "OK"
    

# @app.route('/indications/last')
# @login_required
# def get_online_web():
#     return get_online()

@bp.route('/indications/last')
@login_or_token_required
def get_online_api():
    return get_online()

# @app.route('/indications/<string:id>', methods=['GET'])
# #@login_required
# def get_inds_web(id):
#     return get_inds(id)


@bp.route('/indications/<string:id>', methods=['GET'])
@login_or_token_required
def get_inds_api(id):
    
    return get_inds(id)


def get_inds(id):

    bx = Box.query.where(Box.name==id).first()
	#indications = Indication.query.where(Indication.id_box==bx.id)
    start_time = request.args.get('start')
    end_time = request.args.get('end')


    if start_time is not None or end_time is not None:
        indications = Indication.query.where(Indication.id_box==bx.id).filter(Indication.time > datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S"), Indication.time < datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S"), Indication.time < datetime.now()).order_by(Indication.id)
    else:
        indications = Indication.query.where(Indication.id_box==bx.id).filter(Indication.time > datetime.now()-timedelta(hours=1), Indication.time < datetime.now()).order_by(Indication.id)


    
    indata = []
    i=0
    for ind in indications:
        

        indata.append({
            "id_box": ind.onBox.id,
            "name": ind.onBox.name,
            "temp": ind.temp,
            "hum": ind.hum,
            "time": ind.time.strftime("%Y-%m-%dT%H:%M:%S")
        })
        

    
    # for ind in inds:
    # 	strin+=str(ind.temp) + " " + str(ind.hum) + " " + str(ind.onBox.name) + "\n" + "|"
    return jsonify(indata)


def get_online():
    # inds = db.session.query(Indication.id_box, Box.name,
	# 	Indication.temp, Indication.hum,
	# 	func.max(Indication.time).label("time")).join(Box, Indication.id_box==Box.id).group_by(Indication.id_box, Box.name, Indication.temp, Indication.hum).filter(Indication.time > datetime.now()-timedelta(hours=24))

    max_time = db.session.query(Indication.id_box.label("bx"), func.max(Indication.time).label("tm")).group_by(Indication.id_box).cte(name="max_time", recursive=True)

    last_inds = db.session.query(Indication.id_box, Box.name, Indication.temp, Indication.hum, Indication.time).join(max_time, Indication.id_box == max_time.c.bx).join(Box, Box.id == Indication.id_box).where(Indication.time == max_time.c.tm).filter(Indication.time > datetime.now()-timedelta(hours=1))


    if not last_inds:
        return []

    data = []

    for i in last_inds:
        data.append({
            "id_box": i.id_box,
            "name": i.name,
            "temp": i.temp,
            "hum": i.hum,
            "time": i.time.strftime("%Y-%m-%dT%H:%M:%S")
        })
    return jsonify(data)


def check_temp(box, temp, date):
    if float(temp) > 38.5 or float(temp) < 37.5:
        notifications.send_to_all(box.name, "Выход за пределы рабочей температуры!")
        new_alert = Alert(onBox = box, title = box.name, body = "Выход за пределы рабочей температуры!", date = date)
        return new_alert
    
    return None
    


def check_hum(box, hum, date):
    if float(hum) > 75 or float(hum) < 65:
        notifications.send_to_all(box.name, "Выход за пределы рабочей влажности!")
        new_alert = Alert(onBox = box, title = box.name, body = "Выход за пределы рабочей влажности!", date = date)
        return new_alert
    
    return True

@bp.route("/sensor_fault", methods=['POST'])
@token_auth.login_required
def sensor_fault():
    data = request.get_json()
    device_fault = Device.query.where(Device.address==data["addr"]).first()
    box_fault = Box.query.where(Box.id_device == device_fault.id)

    new_alert = Alert(title = box_fault.name, body='Ошибка чтения')

    return "OK"