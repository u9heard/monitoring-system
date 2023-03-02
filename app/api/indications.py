from app.api import bp
from app.models import Indication
from app.models import Box
from app.api.errors import bad_request
from flask import jsonify, request
from datetime import datetime, timedelta

@bp.route('/indications/<string:id>', methods=['GET'])
def get_inds(id):

    start_time = request.args.get('start')
	
    end_time = request.args.get('end')
	
    bx = Box.query.where(Box.name==id).first()

    if bx is None:
        return bad_request('Invalid name')
	
    if start_time is not None and end_time is not None:
        indications = Indication.query.where(Indication.id_box==bx.id).filter(Indication.time > datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S"), Indication.time < datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S"), Indication.time < datetime.now())
    else:
        indications = Indication.query.where(Indication.id_box==bx.id).filter(Indication.time > datetime.now()-timedelta(hours=1), Indication.time < datetime.now())

    data = Indication.to_collection_dict(indications)
    
    

    return jsonify(data)