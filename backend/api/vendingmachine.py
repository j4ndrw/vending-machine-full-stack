import datetime
import json
from typing import Dict

import jwt
from flask import Flask, Response, request
from models.product import Product
from models.role import USER_ROLES
from models.user import User
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker

from api.auth.auth import create_token, get_token_from_headers, hash_password, verify_auth
from api.utils import handle_exc, log_endpoint, validate_payload

API_CONFIG = {
    "app": None,
    "db_session": None
}


class VendingMachine:
    def __init__(self, app: Flask):
        self.app = app

        # Init engine
        self.engine = create_engine(
            app.config['DATABASE_URI'],
            convert_unicode=True,
            echo=True
        )

        # Init session
        self.db_session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=True,
                bind=self.engine
            )
        )

        API_CONFIG.update({
            "app": self.app,
            "db_session": self.db_session
        })

        # Create tables from schemas if they don't exist
        User.metadata.create_all(bind=self.engine)
        Product.metadata.create_all(bind=self.engine)

    @handle_exc
    @validate_payload(
        necessary_keys=[
            "username",
            "password",
            "role"
        ]
    )
    @log_endpoint
    def register(self) -> Response:
        payload: Dict = request.get_json()

        username = payload["username"]
        password = payload["password"]
        role = payload["role"]

        password = hash_password(password)

        user = self.db_session.query(User)\
            .filter_by(username=username)\
            .first()

        if user:
            return Response(
                json.dumps({
                    "message": "There is already a user with this username!"
                }),
                mimetype="application/json",
                status="403"
            )

        if role not in USER_ROLES:
            return Response(
                json.dumps({
                    "message": "The user must be a buyer or a seller!"
                }),
                mimetype="application/json",
                status="403"
            )

        user = User(
            username=username,
            password=password,
            role=role,
        )

        token = create_token(self.app, user.username)

        self.db_session.add(user)
        self.db_session.commit()

        return Response(
            json.dumps({
                "message": f"Thanks for registering, {username}!",
                "token": token,
            }),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @log_endpoint
    def refresh_token(self, username: str) -> Response:
        user = self.db_session.query(User)\
            .filter_by(username=username)\
            .first()

        if not user:
            return Response(
                json.dumps({
                    "message": "No such user"
                }),
                mimetype="application/json",
                status="403"
            )

        token = create_token(self.app, user.username)

        self.db_session.add(user)
        self.db_session.commit()

        return Response(
            json.dumps({
                "message": "Token refreshed",
                "token": token,
            }),
            mimetype="application/json",
            status=200
        )

    @validate_payload(
        necessary_keys=[
            "username",
            "password",
        ]
    )
    @log_endpoint
    def login(self):
        payload: Dict = request.get_json()

        username = payload["username"]
        password = payload["password"]

        password = hash_password(password)

        user = self.db_session.query(User)\
            .filter_by(username=username)\
            .first()

        if not user:
            return Response(
                json.dumps({
                    "message": "This user does not exist. Try registering first."
                }),
                mimetype="application/json",
                status="404"
            )

        if password != user.password:
            return Response(
                json.dumps({
                    "message": "Invalid credentials. Please try again."
                }),
                mimetype="application/json",
                status="403"
            )

        if user.logged_in:
            return Response(
                json.dumps({
                    "message": f"Welcome, {username}!",
                    "token": (
                        get_token_from_headers(request)
                        or
                        create_token(self.app, username)
                    )
                }),
                mimetype="application/json",
                status=200
            )

        token = create_token(self.app, user.username)

        user.logged_in = True

        self.db_session.commit()

        return Response(
            json.dumps({
                "message": f"Welcome, {username}!",
                "token": token
            }),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @validate_payload(necessary_keys=["username"])
    @log_endpoint
    def logout(self):
        payload: Dict = request.get_json()

        username = payload["username"]

        user = self.db_session.query(User)\
            .filter_by(username=username)\
            .first()

        if not user:
            return Response(
                json.dumps({
                    "message": "This user does not exist. Try registering first."
                }),
                mimetype="application/json",
                status="404"
            )

        if not user.logged_in:
            return Response(
                json.dumps({
                    "message": "You're already logged out"
                }),
                mimetype="application/json",
                status="404"
            )

        user.logged_in = False

        self.db_session.commit()

        return Response(
            json.dumps({
                "message": f"Get back soon, {username}!",
            }),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @log_endpoint
    def get_current_user(self, username: str) -> Response:
        user = self.db_session.query(User)\
            .filter_by(username=username)\
            .first()

        if not user:
            return Response(
                json.dumps({
                    "message": "No such user"
                }),
                mimetype="application/json",
                status="404"
            )

        return Response(
            json.dumps(user.to_json()),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @log_endpoint
    def get_users(self) -> Response:
        users = self.db_session.query(User)

        return Response(
            json.dumps({
                "users": [*map(
                    lambda user: user.to_json(),
                    users.all()
                )]
            }),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @validate_payload(necessary_keys=["role"])
    @log_endpoint
    def update_user_role(self, username: str) -> Response:
        payload = request.get_json()

        role = payload["role"]

        if role not in USER_ROLES:
            return Response(
                json.dumps({
                    "message": "The user must be a buyer or a seller!"
                }),
                mimetype="application/json",
                status="403"
            )

        user = self.db_session.query(User)\
            .filter_by(username=username)\
            .first()

        if not user:
            return Response(
                json.dumps({"message": "No such user"}),
                mimetype="application/json",
                status=404
            )

        user.role = role

        self.db_session.commit()

        return Response(
            json.dumps({"message": "User role updated successfully"}),
            mimetype="application/json",
            status=200
        )
