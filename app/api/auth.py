from functools import wraps
from flask import g, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask_login import login_required
from app.models import User
from app.api.errors import error_responce

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


def login_or_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return login_required(f)(*args, **kwargs)
        return token_auth.login_required(f)(*args, **kwargs)
    return decorated_function


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False;
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    return error_responce(401)

@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
    return error_responce(401)