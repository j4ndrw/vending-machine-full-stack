import json
from typing import Dict, Optional

from flask import Flask, Response, request
from models.product import Product
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

from api.auth.auth import (create_token, get_token_from_headers, hash_password,
                           verify_auth)
from api.operation import Operation
from api.retrieval import Retrieval
from api.utils import handle_exc, log_endpoint

API_CONFIG = {
    "app": None,
    "db_session": None
}


class VendingMachine:
    def __init__(
        self,
        app: Optional[Flask] = None,
        engine: Optional[Engine] = None,
        db_session: Optional[scoped_session] = None
    ):
        self.app = app
        if app:
            self.engine = create_engine(
                app.config['DATABASE_URI'],
                convert_unicode=True,
                echo=True
            )
            self.db_session = scoped_session(
                sessionmaker(
                    autocommit=False,
                    autoflush=True,
                    bind=self.engine
                )
            )
        else:
            self.engine = engine
            self.db_session = db_session

        API_CONFIG.update({
            "app": self.app,
            "db_session": self.db_session
        })

        if self.engine:
            # Create tables from schemas if they don't exist
            User.metadata.create_all(bind=self.engine)
            Product.metadata.create_all(bind=self.engine)

        self.retrieval = Retrieval(self.db_session)
        self.operation = Operation(self.db_session)

    @handle_exc
    @log_endpoint
    def register(self) -> Response:
        payload: Dict = request.get_json()

        username = payload["username"]
        password = payload["password"]
        role = payload["role"]

        password = hash_password(password)

        user, _ = self.retrieval.get_user(username)
        if user:
            return Response(
                json.dumps({
                    "message": "There is already a user registered with this username"
                }),
                mimetype="application/json",
                status="403"
            )

        err = self.operation.validate_role(role)
        if err:
            return err

        user = User(
            username=username,
            password=password,
            role=role,
        )

        self.db_session.add(user)
        self.db_session.commit()

        return Response(
            json.dumps({
                "message": f"Thanks for registering, {username}!",
            }),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG, strict=True, allow_expired=True)
    @handle_exc
    @log_endpoint
    def refresh_token(self, username: str) -> Response:
        user, err = self.retrieval.get_user(username)
        if err:
            return err

        token = create_token(self.app, user.username)

        self.db_session.add(user)
        self.db_session.commit()

        return Response(
            json.dumps({
                "message": "Token refreshed",
                "token": token,
                "username": username
            }),
            mimetype="application/json",
            status=200
        )

    @handle_exc
    @log_endpoint
    def login(self):
        payload: Dict = request.get_json()

        username = payload["username"]
        password = payload["password"]

        password = hash_password(password)

        user, err = self.retrieval.get_user(
            username,
            err_msg="This user does not exist. Try registering first."
        )
        if err:
            return err

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

    @verify_auth(API_CONFIG, strict=True)
    @log_endpoint
    def logout(self):
        payload: Dict = request.get_json()

        username = payload["username"]

        user, err = self.retrieval.get_user(
            username,
            err_msg="This user does not exist. Try registering first."
        )
        if err:
            return err

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

    @verify_auth(API_CONFIG, strict=True)
    @handle_exc
    @log_endpoint
    def get_current_user(self, username: str) -> Response:
        user, err = self.retrieval.get_user(username)
        if err:
            return err

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

    @verify_auth(API_CONFIG, strict=True)
    @handle_exc
    @log_endpoint
    def update_user_role(self, username: str) -> Response:
        payload = request.get_json()

        role = payload["role"]

        err = self.operation.validate_role(role)
        if err:
            return err

        user, err = self.retrieval.get_user(username)
        if err:
            return err

        user.role = role

        self.db_session.commit()

        return Response(
            json.dumps({"message": "User role updated successfully"}),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG, strict=True)
    @handle_exc
    @log_endpoint
    def delete_account(self, username: str) -> Response:
        user, err = self.retrieval.get_user(username)
        if err:
            return err

        self.db_session.delete(user)
        self.db_session.commit()

        return Response(
            json.dumps(
                {"message": "We're sorry to see you going... Hope you get back soon!"}),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG, strict=True)
    @handle_exc
    @log_endpoint
    def create_product(self) -> Response:
        payload = request.get_json()

        username = payload["username"]
        cost = payload["cost"]
        product_name = payload["product_name"]

        err = self.operation.validate_credits(cost, kind="cost")
        if err:
            return err

        if cost < 0:
            return Response(
                json.dumps({"message": "The cost must be positive or 0!"}),
                mimetype="application/json",
                status=400
            )

        user, err = self.retrieval.get_user(username)
        if err:
            return err

        err = self.operation.validate_seller_role(user.role)

        existing_product = self.db_session.query(Product)\
            .filter_by(
                seller_id=user.username,
                product_name=product_name
        )\
            .first()

        if existing_product:
            existing_product.amount_available += 1
            existing_product.cost = cost
            self.db_session.commit()

            return Response(
                json.dumps({
                    "message": f"Product added successfully ({existing_product.amount_available} products)"
                }),
                mimetype="application/json",
                status=200
            )

        product = Product(
            cost=cost,
            product_name=product_name,
            seller_id=user.username
        )

        self.db_session.add(product)
        self.db_session.commit()

        return Response(
            json.dumps({"message": "New product added successfully"}),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @log_endpoint
    def get_product(self, product_id) -> Response:
        product, err = self.retrieval.get_product(product_id)
        if err:
            return err

        return Response(
            json.dumps(product.to_json()),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @log_endpoint
    def get_products(self) -> Response:
        products = self.db_session.query(Product)

        return Response(
            json.dumps({
                "products": [*map(
                    lambda user: user.to_json(),
                    products.all()
                )]
            }),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @log_endpoint
    def get_products_from_user(self, username: str) -> Response:
        user, err = self.retrieval.get_user(username)
        if err:
            return err

        products = self.retrieval.get_products_from_user(
            username,
            role=user.role
        )

        return Response(
            json.dumps({"products": products}),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @log_endpoint
    def delete_product(self, product_id: str) -> Response:
        payload = request.get_json()

        username = payload["username"]

        user, err = self.retrieval.get_user(username)
        if err:
            return err

        if user.role != "seller":
            return Response(
                json.dumps({"message": "Only sellers can delete products!"}),
                mimetype="application/json",
                status=403
            )

        product, err = self.retrieval.get_product(product_id)
        if err:
            return err

        if product.seller_id != user.username:
            return Response(
                json.dumps(
                    {"message": "You are not the owner of this product!"}),
                mimetype="application/json",
                status=403
            )

        self.db_session.delete(product)
        self.db_session.commit()

        return Response(
            json.dumps({"message": "Product deleted successfully!"}),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @log_endpoint
    def update_product(self, product_id: str):
        payload = request.get_json()

        username = payload["username"]
        cost = payload["cost"]
        product_name = payload["product_name"]

        err = self.operation.validate_credits(cost, kind="cost")
        if err:
            return err

        user, err = self.retrieval.get_user(username)
        if err:
            return err

        if user.role != "seller":
            return Response(
                json.dumps({"message": "Only sellers can update products!"}),
                mimetype="application/json",
                status=403
            )

        product, err = self.retrieval.get_product(product_id)
        if err:
            return err

        if product.seller_id != user.username:
            return Response(
                json.dumps(
                    {"message": "You are not the owner of this product!"}),
                mimetype="application/json",
                status=403
            )

        product.cost = cost
        product.product_name = product_name

        self.db_session.commit()

        return Response(
            json.dumps({"message": "Product updated successfully!"}),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @log_endpoint
    def deposit(self) -> Response:
        payload = request.get_json()

        username = payload["username"]
        deposit = payload["deposit"]

        err = self.operation.validate_credits(deposit, kind="deposit")
        if err:
            return err

        user, err = self.retrieval.get_user(username)
        if err:
            return err

        err = self.operation.validate_depositer_role(user.role)
        if err:
            return err

        user.deposit += deposit

        self.db_session.commit()

        return Response(
            json.dumps(
                {"message": f"You've successfully deposited {deposit} credits!"}),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @log_endpoint
    def buy(self) -> Response:
        payload = request.get_json()

        username = payload["username"]
        total = payload["total"]
        product_ids = payload["product_ids"]

        err = self.operation.validate_credits(total, kind="total")
        if err:
            return err

        user, err = self.retrieval.get_user(username)
        if err:
            return err

        err = self.operation.validate_buyer_role(user.role)
        if err:
            return err

        if user.deposit < total:
            return Response(
                json.dumps({"message": "Insufficient funds!"}),
                mimetype="application/json",
                status=403
            )

        user.deposit -= total

        self.operation.reduce_product_stock(product_ids)

        self.db_session.commit()

        return Response(
            json.dumps(
                {
                    "message": f"Thank you for purchasing from us!",
                    "amount_spent": total
                }),
            mimetype="application/json",
            status=200
        )

    @verify_auth(API_CONFIG)
    @handle_exc
    @log_endpoint
    def reset_deposit(self) -> Response:
        payload = request.get_json()

        username = payload["username"]

        user, err = self.retrieval.get_user(username)
        if err:
            return err

        err = self.operation.validate_depositer_role(user.role)
        if err:
            return err

        user.deposit = 0

        self.db_session.commit()

        return Response(
            json.dumps(
                {"message": f"You've successfully reset your deposit!"}),
            mimetype="application/json",
            status=200
        )
