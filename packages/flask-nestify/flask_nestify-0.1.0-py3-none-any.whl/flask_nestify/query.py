import inspect
import types
from flask import request
from .logger import nestpy_logger
from .globals import queries_map
from .utils import get_func_key


class QueryProcessor:
    def __init__(self, func: types.FunctionType) -> None:
        self.func = func
        self.key = get_func_key(self.func)
        self.queries = []
        if self.key in queries_map:
            self.queries = queries_map[self.key]

    def process(self, kwargs):
        args = request.args
        params = inspect.signature(self.func).parameters
        for query in self.queries:
            param_name = query["name"]
            param_default = None
            param_type = str
            if param_name in params:
                param = params[param_name]
                if param.annotation != param.empty:
                    param_type = param.annotation
                if param.default != param.empty:
                    param_default = param.default
                kwargs[query["name"]] = args.get(
                    query["name"], param_default, param_type
                )
            else:
                nestpy_logger.warning(
                    f"Query parameter {param_name} not defined in function {self.func.__name__}"
                )
