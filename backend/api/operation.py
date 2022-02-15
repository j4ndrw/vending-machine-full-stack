import json
from typing import Any, List, Optional

from flask import Response
from models.product import Product
from models.role import USER_ROLES
from sqlalchemy.orm import scoped_session

from api.utils import Error


class Operation:
    def __init__(self, db_session: Optional[scoped_session] = None):
        self.db_session = db_session

    def validate_role(self, role: str) -> Optional[Error]:
        if role not in USER_ROLES:
            return Response(
                json.dumps({
                    "message": "The user must be a buyer or a seller!"
                }),
                mimetype="application/json",
                status="403"
            )
        return None

    def validate_deposit(self, credits: int) -> Optional[Error]:
        allowed_top_up = [5, 10, 20, 50, 100]
        stringed_allow_top_up = ", ".join(
            [*map(lambda item: str(item), allowed_top_up)])

        if credits not in allowed_top_up:
            return Response(
                json.dumps(
                    {"message": f"You can only deposit {stringed_allow_top_up} credits!"}),
                mimetype="application/json",
                status=400
            )

        return None

    def validate_total(self, credits: int) -> Optional[Error]:
        if credits <= 0:
            return Response(
                json.dumps(
                    {"message": "The total must be a positive amount"}),
                mimetype="application/json",
                status=400
            )
        return None

    def validate_credits(self, credits: Any, kind: str) -> Optional[Error]:
        if not isinstance(credits, int):
            return Response(
                json.dumps({"message": f"The {kind} must be an integer!"}),
                mimetype="application/json",
                status=400
            )

        if kind == "deposit":
            return self.validate_deposit(credits)

        if kind == "total":
            return self.validate_total(credits)

        return None

    def validate_depositer_role(self, role: str) -> Optional[Error]:
        if role != "buyer":
            return Response(
                json.dumps({"message": "Only buyers can deposit money!"}),
                mimetype="application/json",
                status=403
            )
        return None

    def validate_buyer_role(self, role: str) -> Optional[Error]:
        if role != "buyer":
            return Response(
                json.dumps({"message": "Only buyers can buy!"}),
                mimetype="application/json",
                status=403
            )
        return None

    def validate_seller_role(self, role: str) -> Optional[Error]:
        if role != "seller":
            return Response(
                json.dumps({"message": "Only seller can create products!"}),
                mimetype="application/json",
                status=403
            )
        return None

    def reduce_product_stock(self, product_ids: List[int]):
        product_query = self.db_session.query(Product)
        for product_id in product_ids:
            product_query.filter_by(id=product_id)

        products = product_query.all()
        for product in products:
            if product.amount_available <= 1:
                self.db_session.delete(product)
            else:
                product.amount_available -= 1
