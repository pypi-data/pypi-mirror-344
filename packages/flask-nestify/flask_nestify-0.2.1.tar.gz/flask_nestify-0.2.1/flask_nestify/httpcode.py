import types

import flask
from .logger import DEBUG, nestpy_logger
from .utils import get_func_key
from .globals import http_code_map


class HttpCode:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code

    def __call__(self, func):
        nestpy_logger.log(DEBUG, f"Add to response: {func}")
        key = get_func_key(func)
        if key not in http_code_map:
            http_code_map[key] = {
                "status_code": self.status_code,
            }
        else:
            nestpy_logger.log(DEBUG, "HttpCode decorator already defined")
        return func


class HttpCodeProcessor:
    def __init__(self, func: types.FunctionType) -> None:
        self.func = func
        self.key = get_func_key(self.func)
        self.httpCode = 200
        if self.key in http_code_map:
            self.httpCode = http_code_map[self.key]

    def process(self, kwargs, response: flask.Response):
        if isinstance(self.httpCode, dict) and "status_code" in self.httpCode:
            response.status = self.httpCode["status_code"]
        else:
            response.status = self.httpCode
