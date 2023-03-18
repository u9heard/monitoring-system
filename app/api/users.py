from app.api import bp
from app.api.auth import token_auth
from flask import jsonify, request, g
from app.models import User
from app import app, db
from flask_login import login_required, current_user



@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@app.route('/fcmtoken', methods=['POST'])
@login_required
def add_fcm():
    cur_token = current_user.fcmtoken

    data = request.get_json()
    if(data['fcm'] is not None and data['fcm'] != cur_token):
        current_user.set_fcm(data['fcm'])
        db.session.commit()
        return 'added'

    return 'ok'

@app.route('/test')
@login_required
def test():
    cur_user = current_user
    return """{0} {1} {2}""".format(cur_user.username, cur_user.token, cur_user.email)