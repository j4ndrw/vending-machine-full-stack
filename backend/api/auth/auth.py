import json
from datetime import datetime, timedelta
from functools import wraps
from hashlib import sha256
from typing import Union

import jwt
from flask import Flask, Response, request, Request
from models.user import User
from sqlalchemy.orm import scoped_session


def hash_password(password: Union[str, int]) -> str:
    return sha256(str(password).encode()).hexdigest()


def create_token(app: Flask, username: str) -> str:
    return jwt.encode({
        'username': username,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, app.config['SECRET'])


def get_token_from_headers(request: Request) -> str:
    return request.headers["x-access-token"]


def validate_jwt(app: Flask, db_session: scoped_session):
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
        data = jwt.decode(token, app.config['SECRET'])
        current_user = db_session.query(User)\
            .filter_by(username=data['username'])\
            .first()

        if current_user is None:
            return Response(
                json.dumps({'message': 'Token is invalid!'}),
                mimetype="application/json",
                status=401
            )

        current_time = datetime.utcnow().timestamp()
        if data["exp"] - current_time > 0:
            return Response(
                json.dumps(
                    {'message': 'Session expired. Please login again.'}),
                mimetype="application/json",
                status=409
            )

    except Exception:
        return Response(
            json.dumps({'message': 'Token is invalid!'}),
            mimetype="application/json",
            status=401
        )


def verify_auth(f):
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
                data = jwt.decode(token, app.config['SECRET'])
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
