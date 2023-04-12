from flask_login import login_required
from app.api import bp
from app.api.auth import token_auth
from app.models import Box, Device
from app.api.errors import bad_request
from flask import jsonify, request, g, render_template
from datetime import datetime, timedelta
from app import app, db



@app.route('/config/replace', methods=['POST'])
@login_required
def replace_addr_web():
    return replace_addr()


@bp.route('/config/replace', methods=['POST'])

def replace_addr_api():
    return replace_addr()

@bp.route('/config', methods=['GET'])
@token_auth.login_required
def configuration_api():
    devices = db.session.query(Box.id, Device.address, Box.name).join(Device, Device.id == Box.id_device, isouter = True).order_by(Box.id)

    addr_list = []

    for a in devices:
        addr_list.append({
            "box_id": a.id,
            "address": a.address,
            "box_name": a.name
        })

    dev_list = ['Не заменять', 'None']
    [dev_list.append(d.address) for d in Device.query.all()]

    return jsonify({"addresses": addr_list, "dev_list":dev_list})


@bp.route('/devices', methods=['GET'])
@token_auth.login_required
def get_devices():
    devices = Device.query.all()
    
    device_list = []

    for a in devices:
        device_list.append({
            "id": a.id,
            "address": a.address,
            "correction_t": a.correction_t,
            "correction_h": a.correction_h
        })


    return jsonify(device_list)


@app.route('/config', methods=['GET'])
@login_required
def configuration_web():
    devices = db.session.query(Box.id, Device.address, Box.name).join(Device, Device.id == Box.id_device, isouter = True).order_by(Box.id)

    dev_addr = Device.query.all()

    dev_list = ['Не заменять', 'None']
    [dev_list.append(d.address) for d in Device.query.all()]


    return render_template('config.html', devices=devices, dev_list=dev_list, dev_addr=dev_addr)



def replace_addr():
    req_data = request.json
    
    if "box" in req_data:
        for req in req_data["box"]:
            if req["addr"] != "Не заменять":  
                if req["addr"] == 'None':
                    db.session.query(Box).filter(Box.id == req["id"]).update({Box.id_device: None})
                    

                else:

                    device_id = Device.query.where(Device.address == req["addr"]).first()

                    db.session.query(Box).filter(Box.id == req["id"]).update({Box.id_device: device_id.id})
                    # db.session.commit()

    if "device" in req_data:
        for req in req_data["device"]:
            db.session.query(Device).filter(Device.id == req["id"]).update({Device.correct_t: req["correction_t"],
                                                                            Device.correct_h: req["correction_h"]})
    
    if check_uniq(Box.query.all()) == False:
        return jsonify({"result": "Uniq error"})  

    db.session.commit()
    return jsonify({"result": "OK"})  


def check_uniq(boxes):
    for box in boxes:
        for box_u in boxes:
            if box.id_device == box_u.id_device and box.id_device != None and box.id != box_u.id:
                return False
    
    return True
