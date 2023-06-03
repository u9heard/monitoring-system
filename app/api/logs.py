from flask_login import login_required
from app.api import bp
from app.api.auth import token_auth, login_or_token_required
from app.models import Log, Alert
from app.api.errors import bad_request
from flask import jsonify, request, g
import os


@bp.route('/logs', methods=['GET'])
@login_or_token_required
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

@bp.route('/logs/<int:id>', methods=['GET'])
@login_or_token_required
def get_log_by_id(id):
    log = Log.query.get_or_404(id)

    if os.path.exists(log.path):

        with open(log.path, 'r') as file:
            content = file.read()
        return content
    else:
        return 404


    #     id = db.Column(db.Integer, primary_key = True)
	# name = db.Column(db.String(64))
	# date = db.Column(db.String(64))
	# path = db.Column(db.String(64))