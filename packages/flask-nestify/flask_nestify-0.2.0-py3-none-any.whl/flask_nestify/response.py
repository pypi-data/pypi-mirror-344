import inspect
import json
import types
import flask

from .exception import InternalServerErrorException
from .logger import DEBUG, nestpy_logger
from .utils import get_func_key
from .globals import response_map
from abc import ABC, ABCMeta, abstractmethod


class Response:
    def __init__(
        self,
        name,
    ):
        self.name = name

    def __call__(self, func):
        nestpy_logger.log(DEBUG, f"Add to response: {func}")
        key = get_func_key(func)
        if key not in response_map:
            response_map[key] = {
                "name": self.name,
            }
        else:
            nestpy_logger.log(DEBUG, "Response decorator already defined")
        return func


class ResponseProcessor:
    def __init__(self, func: types.FunctionType) -> None:
        self.func = func
        self.key = get_func_key(self.func)
        self.response = None
        if self.key in response_map:
            self.response = response_map[self.key]

    def process(self, kwargs, res):
        if self.response:
            params = inspect.signature(self.func).parameters
            response_param_name = self.response["name"]
            if response_param_name in params:
                kwargs[response_param_name] = res


class JsonSerializable(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "toJSON")
            and (callable(subclass.toJSON) or NotImplemented)
        ) or (
            hasattr(subclass, "to_json")
            and (callable(subclass.to_json) or NotImplemented)
        )


class ResponseMiddleware(ABC):
    def __init__(self) -> None:
        pass

    def is_json(self, str_value):
        try:
            json.loads(str_value)
        except ValueError as e:
            return False
        return True

    @abstractmethod
    def response_str(
        self, response: flask.Response, func_response: str
    ) -> flask.Response:
        """ "Not implemented yet"""

    @abstractmethod
    def response_int(
        self, response: flask.Response, func_response: int
    ) -> flask.Response:
        """ "Not implemented yet"""

    @abstractmethod
    def response_tuple(
        self, response: flask.Response, func_response: tuple
    ) -> flask.Response:
        """ "Not implemented yet"""

    @abstractmethod
    def response_dict(
        self, response: flask.Response, func_response: dict
    ) -> flask.Response:
        """ "Not implemented yet"""

    @abstractmethod
    def response_list(
        self, response: flask.Response, func_response: list
    ) -> flask.Response:
        """ "Not implemented yet"""

    @abstractmethod
    def response_flask_response(
        self, response: flask.Response, func_response: flask.Response
    ) -> flask.Response:
        """ "Not implemented yet"""

    @abstractmethod
    def response_unknown(
        self, response: flask.Response, func_response
    ) -> flask.Response:
        """ "Not implemented yet"""

    @abstractmethod
    def response_object(
        self, response: flask.Response, func_response
    ) -> flask.Response:
        """ "Not implemented yet"""

    def get_response(self, response: flask.Response, func_response):
        if isinstance(func_response, str):
            return self.response_str(response, func_response)
        elif isinstance(func_response, int):
            return self.response_int(response, func_response)
        elif isinstance(func_response, tuple):
            return self.response_tuple(response, func_response)
        elif isinstance(func_response, dict):
            return self.response_dict(response, func_response)
        elif isinstance(func_response, list):
            return self.response_list(response, func_response)
        elif isinstance(func_response, flask.Response):
            return self.response_flask_response(response, func_response)
        elif hasattr(func_response, "__dict__"):
            return self.response_object(response, func_response)
        else:
            return self.response_unknown(response, func_response)


class DefaultResponse(ResponseMiddleware):
    def response_str(
        self, response: flask.Response, func_response: str
    ) -> flask.Response:
        response.response = func_response
        return response

    def response_int(
        self, response: flask.Response, func_response: int
    ) -> flask.Response:
        response.response = str(func_response)
        return response

    def response_object(
        self, response: flask.Response, func_response
    ) -> flask.Response:
        response.content_type = "application/json"
        if self.is_json(str(func_response)):
            response.response = str(func_response)
            return response

        def dumper(obj):
            if issubclass(obj.__class__, JsonSerializable):
                return obj.toJSON() if hasattr(obj, "toJSON") else obj.to_json()
            return obj.__dict__

        response.response = json.dumps(func_response, default=dumper)
        return response

    def response_tuple(
        self, response: flask.Response, func_response: tuple
    ) -> flask.Response:
        if not isinstance(func_response[0], tuple):
            response = self.get_response(response, func_response[0])
        else:
            response.response = str(func_response[0])
        response.status_code = int(func_response[1])
        return response

    def response_dict(self, response: flask.Response, func_response: dict):
        def dumper(obj):
            if issubclass(obj.__class__, JsonSerializable):
                return obj.toJSON() if hasattr(obj, "toJSON") else obj.to_json()
            return obj.__dict__

        response.response = json.dumps(func_response, default=dumper)
        response.content_type = "application/json"
        return response

    def response_flask_response(
        self, response: flask.Response, func_response: flask.Response
    ) -> flask.Response:
        return func_response

    def response_list(
        self, response: flask.Response, func_response: list
    ) -> flask.Response:
        def dumper(obj):
            if issubclass(obj.__class__, JsonSerializable):
                return obj.toJSON() if hasattr(obj, "toJSON") else obj.to_json()
            return obj.__dict__

        response.response = json.dumps(func_response, default=dumper)
        response.content_type = "application/json"
        return response

    def response_unknown(
        self, response: flask.Response, func_response
    ) -> flask.Response:
        raise InternalServerErrorException("Unknown response type")
