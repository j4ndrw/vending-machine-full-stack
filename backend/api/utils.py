from functools import wraps
import traceback
from typing import Callable, Dict, List
from urllib.request import Request

from flask import Response, abort, request
from werkzeug.local import LocalProxy

Error = Response


def handle_exc(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            f = func(*args, **kwargs)
            return f
        except:
            return Response(traceback.format_exc(), 500)

    return wrapper


def log_endpoint(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n\n\t\t\t**Running {func.__name__} endpoint**\n\n")
        return func(*args, **kwargs)
    return wrapper


def _validate_payload(
    request_body: Dict,
    expected_fields: List[str],
    err_status=400,
):
    errors = []

    if request_body is None:
        return ["No body in request"]

    for field in expected_fields:
        if field not in request_body:
            errors.append(f"'{field}' missing from request body")

    if len(errors) > 0:
        abort(
            status=err_status,
            description=f"Bad JSON body: {errors}"
        )
