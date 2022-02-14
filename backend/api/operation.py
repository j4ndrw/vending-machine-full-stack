from api.utils import Error
from typing import Any, Optional
from flask import Response
from sqlalchemy.orm import scoped_session

from models.role import USER_ROLES
import json


class Operation:
    def __init__(self, db_session: scoped_session):
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

    def validate_credits(self, credits: Any, kind: str) -> Optional[Error]:
        if not isinstance(credits, int):
            return Response(
                json.dumps({"message": f"The {kind} must be an integer!"}),
                mimetype="application/json",
                status=400
            )
        return None
