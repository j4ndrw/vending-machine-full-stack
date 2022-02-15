import json
from datetime import datetime, timedelta
from functools import wraps
from hashlib import sha256
import traceback
from typing import Callable, Dict, Optional, Union

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


def get_username_from_request(request: Request) -> Optional[str]:
    json_payload = request.get_json()
    if json_payload and "username" in json_payload:
        return json_payload["username"]

    return request.view_args.get("username", None)


def validate_jwt(
    app: Flask,
    db_session: scoped_session,
    strict: bool = False,
    allow_expired: bool = False
):
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
        data = jwt.decode(token, app.config['SECRET'], algorithms=["HS256"])
        if strict:
            username_from_jwt = data['username']
            username_from_request = get_username_from_request(request)

            if username_from_jwt != username_from_request:
                return Response(
                    json.dumps({"message": "Permission Denied"}),
                    mimetype="application/json",
                    status=403
                )

        current_user = db_session.query(User)\
            .filter_by(username=data['username'])\
            .first()

        if current_user is None:
            return Response(
                json.dumps({'message': 'Token is invalid!'}),
                mimetype="application/json",
                status=401
            )

    except jwt.exceptions.ExpiredSignatureError:
        if allow_expired:
            pass
        else:
            return Response(
                json.dumps(
                    {'message': 'Session expired. Please login again.'}),
                mimetype="application/json",
                status=409
            )

    except Exception as e:
        traceback.print_exc()
        return Response(
            json.dumps({'message': 'Token is invalid!'}),
            mimetype="application/json",
            status=401
        )


def verify_auth(api_config: Dict, strict: bool = False, allow_expired: bool = False):
    def decorator(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            err = validate_jwt(
                api_config["app"],
                api_config["db_session"],
                strict=strict,
                allow_expired=True
            )
            if err:
                return err

            # returns the current logged in users contex to the routes
            return f(*args, **kwargs)

        return wrapper
    return decorator
