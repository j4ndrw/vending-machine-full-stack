import json
from typing import List, Optional, Tuple

from flask import Response
from models.product import Product
from models.user import User
from sqlalchemy.orm import scoped_session

from api.utils import Error


class Retrieval:
    def __init__(self, db_session: scoped_session):
        self.db_session = db_session

    def get_user(
        self,
        username: str,
        err_msg: str = "No such user"
    ) -> Tuple[Optional[User], Optional[Error]]:
        user = self.db_session.query(User)\
            .filter_by(username=username)\
            .first()

        if not user:
            return None, Response(
                json.dumps({"message": err_msg}),
                mimetype="application/json",
                status=404
            )

        return user, None

    def get_product(
        self,
        product_id: int
    ) -> Tuple[Optional[Product], Optional[Error]]:
        product_query = self.db_session.query(Product)
        product = product_query.get(product_id)

        if not product:
            return None, Response(
                json.dumps({"message": "No such product"}),
                mimetype="application/json",
                status=404
            )

        return product, None

    def get_products_from_user(
        self,
        username: str,
        role: str
    ) -> List[Product]:
        if role == "buyer":
            filter_dict = {"buyer_id": username}
        else:
            filter_dict = {"seller_id": username}

        product_query = self.db_session.query(Product)\
                            .filter_by(**filter_dict)

        print(filter_dict)

        return [*map(
            lambda product: product.to_json(),
            product_query.all()
        )]
