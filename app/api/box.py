from flask_login import login_required
from app.api import bp
from app.api.auth import token_auth, login_or_token_required
from app.models import Box
from app.api.errors import bad_request
from flask import jsonify, request, g

@bp.route('/boxes', methods=['GET'])
# @token_auth.login_required
@login_or_token_required
def get_boxes_api():
    boxes = Box.query.order_by(Box.id)

    data_to_send = []

    for box in boxes:
        data_to_send.append({
            "id": box.id,
            "name": box.name
        })

    return jsonify({"boxes": data_to_send})