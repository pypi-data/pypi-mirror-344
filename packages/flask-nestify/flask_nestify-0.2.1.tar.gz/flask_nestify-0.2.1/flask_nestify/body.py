import inspect
import types
from flask import request

from .globals import bodies_map
from .globals import data_transfer_objs
from .utils import build_dto, get_func_key


class BodyProcessor:
    def __init__(self, func: types.FunctionType) -> None:
        self.func = func
        self.key = get_func_key(self.func)
        self.body = None
        if self.key in bodies_map:
            self.body = bodies_map[self.key]

    def build_param(self, cls, kwargs):
        if cls is dict and request.is_json:
            kwargs[self.body["name"]] = request.get_json()
        elif cls is int:
            kwargs[self.body["name"]] = int(request.get_data())
        elif cls is str:
            kwargs[self.body["name"]] = request.get_data().decode("utf-8")
        else:
            kwargs[self.body["name"]] = build_dto(
                data_transfer_objs, request.get_json(), cls
            )

    def process(self, kwargs):
        if self.body:
            params = inspect.signature(self.func).parameters
            body_param_name = self.body["name"]
            if body_param_name in params:
                param = params[body_param_name]
                if param.annotation != param.empty:
                    param_cls = param.annotation
                    self.build_param(param_cls, kwargs)
