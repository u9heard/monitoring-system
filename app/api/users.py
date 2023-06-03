from app.api import bp
from app.api.auth import token_auth, login_or_token_required
from flask import jsonify, request, g
from app.models import User, FCMtokens
from app import app, db
from flask_login import login_required, current_user



@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/fcmtoken', methods=['POST'])
@login_or_token_required
def add_fcm_by_api():
    cur_user = current_user if current_user is not None else g.current_user
    cur_tokens = db.session.query(FCMtokens.fcm_token).where(FCMtokens.id_user == cur_user.id).all()

    data = request.get_json()
    if(data['fcm'] is not None and (data['fcm'],) not in cur_tokens):
            new_fcm = FCMtokens(id_user = cur_user.id, fcm_token = data['fcm'])
            #current_user.set_fcm(data['fcm'])
            db.session.add(new_fcm)
            db.session.commit()
            return 'added'

    return 'ok'

@bp.route('/delete_fcm', methods=['POST'])
@login_or_token_required
def delete_fcm():
    cur_user = current_user if current_user is not None else g.current_user

    data = request.get_json()

    token = FCMtokens.query.where(FCMtokens.fcm_token == data['fcmtoken']).first()

    if token is not None and token.id_user == cur_user.id:
        db.session.delete(token)
        db.session.commit()
    
    return 201