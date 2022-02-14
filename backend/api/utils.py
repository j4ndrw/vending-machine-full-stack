from functools import wraps
import traceback
from typing import Callable, Dict, List
from urllib.request import Request

from flask import Response, abort
from werkzeug.local import LocalProxy


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
        print(f"Running {func.__name__} endpoint")
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

    if errors:
        abort(
            status=err_status,
            description=f"Bad JSON body: {errors}"
        )


def validate_payload(necessary_keys: List[str], err_status=400):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, request_json=None, **kwargs):
            if request_json == None:
                for arg in args:
                    if isinstance(arg, (Request, LocalProxy)):
                        request_json = arg.get_json()
                        print(request_json)
                        break
            else:
                kwargs.update({"request_json": request_json})
            _validate_payload(
                request_json,
                expected_fields=necessary_keys,
                err_status=err_status
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator
