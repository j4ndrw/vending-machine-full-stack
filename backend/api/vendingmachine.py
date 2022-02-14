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

from api.auth.auth import create_token, hash_password, token_required
from api.utils import handle_exc, log_endpoint, validate_payload


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
    def create_user(self) -> Response:
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
                "token": token
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

    @token_required
    @handle_exc
    @log_endpoint
    def get_user(self, username: str) -> Response:
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
