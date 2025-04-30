import inspect
import types
from flask import request
import flask

from .decorator import Decorator
from .logger import DEBUG, nestpy_logger
from .utils import get_func_key
from .globals import headers_map


class HeadersV2(Decorator):
    def __init__(self, name) -> None:
        super().__init__(name=name)

    def post_response(self, response: flask.Response):
        pass

    def pre_response(self, func_kwargs):
        params = inspect.signature(self.func).parameters
        headers_param_name = self.kwargs["name"]
        if headers_param_name in params:
            func_kwargs[headers_param_name] = request.headers


class Headers:
    def __init__(
        self,
        name,
    ):
        self.name = name

    def __call__(self, func):
        nestpy_logger.log(DEBUG, f"Add to headers: {func}")
        key = get_func_key(func)
        if key not in headers_map:
            headers_map[key] = {
                "name": self.name,
            }
        else:
            nestpy_logger.warning(f"Function {func.__name__} already has headers")
        return func


class HeadersProcessor:
    def __init__(self, func: types.FunctionType) -> None:
        self.func = func
        self.key = get_func_key(self.func)
        self.headers = None
        if self.key in headers_map:
            self.headers = headers_map[self.key]

    def process(self, kwargs):
        if self.headers:
            params = inspect.signature(self.func).parameters
            headers_param_name = self.headers["name"]
            if headers_param_name in params:
                kwargs[headers_param_name] = request.headers
