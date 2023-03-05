from app.api import bp
from app.api.auth import token_auth
from flask import jsonify
from app.models import User



@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

