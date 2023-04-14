from flask_login import login_required
from app.api import bp
from app.api.auth import token_auth
from app.models import Log
from app.api.errors import bad_request
from flask import jsonify, request, g


@bp.route('/logs', methods=['GET'])
@token_auth.login_required
def get_logs_api():
    logs = Log.query.order_by(Log.id)

    data_to_send = []

    for log in logs:
        data_to_send.append({
            "id": log.id,
            "name": log.name,
            "data": log.date,
            "path": log.path
        })

    return jsonify({"logs": data_to_send})


    #     id = db.Column(db.Integer, primary_key = True)
	# name = db.Column(db.String(64))
	# date = db.Column(db.String(64))
	# path = db.Column(db.String(64))