from flask_login import login_required
from app.api import bp
from app.api.auth import token_auth
from app.models import Box, Device
from app.api.errors import bad_request
from flask import jsonify, request, g
from datetime import datetime, timedelta
from app import app, db


@app.route('/config/replace', methods=['POST'])
@login_required
def replace_addr():
    req_data = request.json

    for req in req_data["data"]:
        if req["addr"] != "Не заменять":  
            if req["addr"] == 'None':
                db.session.query(Box).filter(Box.id == req["id"]).update({Box.id_device: None})
                db.session.commit()

            else:

                device_id = Device.query.where(Device.address == req["addr"]).first()

                db.session.query(Box).filter(Box.id == req["id"]).update({Box.id_device: device_id.id})
                db.session.commit()
        


    
    return "OK"