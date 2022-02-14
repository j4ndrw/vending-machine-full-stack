from datetime import datetime, timedelta
from functools import wraps
from flask import request, Response, Flask
import json
import jwt

from models.user import User

from hashlib import sha256


def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()


def create_token(app: Flask, username: str) -> str:
    return jwt.encode({
        'username': username,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, app.config['SECRET'])


def token_required(f):
    def parameterized_decorator(app: Flask):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            # jwt is passed in the request header
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            # return 401 if token is not passed
            if not token:
                return Response(
                    json.dumps({'message': 'Token is missing!'}),
                    mimetype="application/json",
                    status=401
                )

            try:
                # decoding the payload to fetch the stored details
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = User.query\
                    .filter_by(username=data['username'])\
                    .first()
            except Exception:
                return Response(
                    json.dumps({'message': 'Token is invalid!'}),
                    mimetype="application/json",
                    status=401
                )

            # returns the current logged in users contex to the routes
            return f(current_user, *args, **kwargs)

        return decorated
    return parameterized_decorator
