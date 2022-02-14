from flask import Flask, Response
from flask_cors import CORS
from flask_dotenv import DotEnv

from api.vendingmachine import VendingMachine

app = Flask(__name__)
env = DotEnv(app)
vending_machine_api = VendingMachine(app)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"]
        }
    }
)


@app.route(
    "/api/vendingmachine/register",
    methods=["POST"]
)
def register() -> Response:
    return vending_machine_api.register()


@app.route(
    "/api/vendingmachine/login",
    methods=["POST"]
)
def login() -> Response:
    return vending_machine_api.login()


@app.route(
    "/api/vendingmachine/logout",
    methods=["PUT"]
)
def logout() -> Response:
    return vending_machine_api.logout()


@app.route(
    "/api/vendingmachine/users/<username>",
    methods=["GET"]
)
def get_current_user(username: str) -> Response:
    return vending_machine_api.get_current_user(username)


@app.route(
    "/api/vendingmachine/users",
    methods=["GET"]
)
def get_users() -> Response:
    return vending_machine_api.get_users()


@app.route(
    "/api/vendingmachine/users/<username>",
    methods=["PUT"]
)
def update_user_role(username: str) -> Response:
    return vending_machine_api.update_user_role(username)


@app.route(
    "/api/vendingmachine/users/<username>",
    methods=["DELETE"]
)
def delete_account(username: str) -> Response:
    return vending_machine_api.delete_account(username)


@app.route(
    "/api/vendingmachine/products",
    methods=["POST"]
)
def create_product() -> Response:
    return vending_machine_api.create_product()


@app.route(
    "/api/vendingmachine/products/<product_id>",
    methods=["GET"]
)
def get_product(product_id: str) -> Response:
    return vending_machine_api.get_product(product_id)


@app.route(
    "/api/vendingmachine/products",
    methods=["GET"]
)
def get_products() -> Response:
    return vending_machine_api.get_products()


@app.route(
    "/api/vendingmachine/products/from/<username>",
    methods=["GET"]
)
def get_products_from_user(username: str) -> Response:
    return vending_machine_api.get_products_from_user(
        username
    )


@app.route(
    "/api/vendingmachine/products/<product_id>",
    methods=["PUT"]
)
def update_product(product_id: str) -> Response:
    return vending_machine_api.update_product(product_id)


@app.route(
    "/api/vendingmachine/products/<product_id>",
    methods=["DELETE"]
)
def delete_product(product_id: str) -> Response:
    return vending_machine_api.delete_product(product_id)


@app.route(
    "/api/vendingmachine/deposit",
    methods=["PUT"]
)
def deposit() -> Response:
    return vending_machine_api.deposit()


@app.route(
    "/api/vendingmachine/buy",
    methods=["PUT"]
)
def buy() -> Response:
    return vending_machine_api.buy()


@app.route(
    "/api/vendingmachine/deposit/reset",
    methods=["PUT"]
)
def reset_deposit() -> Response:
    return vending_machine_api.reset_deposit()


@app.route(
    "/api/vendingmachine/token/refresh/<username>",
    methods=["GET"]
)
def refresh_token(username: str) -> Response:
    return vending_machine_api.refresh_token(username)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
