import base64
import inspect
from abc import ABC, abstractmethod
import re
from typing import Any, Callable, Dict, TypedDict, Union
from colorama import Fore
import flask

from .pipe import PipeTransform
from .utils import get_class_key, get_func_key
from .globals import controllers
from .globals import injectables
from .globals import methods_map
from .globals import queries_map
from .globals import bodies_map
from .globals import pipes_map
from .globals import data_transfer_objs
from .globals import decorators
from .globals import ready
from .logger import DEBUG, nestpy_logger
from .exception import BadRequestException


class Decorator(ABC):
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.func = None

    def __call__(self, func):
        self.func = func
        # print("Decorator", func)
        key = get_func_key(func)
        if key not in decorators:
            decorators[key] = []
        decorators[key].append(
            {"args": self.args, "kwargs": self.kwargs, "decorator": self}
        )
        return func

    @abstractmethod
    def pre_response(self, func_kwargs):
        """Not implemented yet"""

    @abstractmethod
    def post_response(self, response: flask.Response):
        """Not implemented yet"""


# TODO: Implement CustomHeader decorator
# class CustomHeader(Decorator):
#     def __init__(self, name) -> None:
#         super().__init__(name=name)

#     def post_response(self, response: flask.Response):
#         response.headers["X-Custom"] = "custom"


class BasicAuth(Decorator):
    def __init__(self, name, validation: Callable[[str, str], Any]) -> None:
        super().__init__(name=name)
        self.validation = validation

    def post_response(self, response: flask.Response):
        pass

    def pre_response(self, func_kwargs):
        params = inspect.signature(self.func).parameters
        headers_param_name = self.kwargs["name"]
        if headers_param_name not in params:
            return
        authorization: str = flask.request.headers.get("Authorization")
        if not authorization:
            pre_response = self.validation(None, None)
            func_kwargs[headers_param_name] = pre_response
            return pre_response
        value = re.search(r"[B|b]asic (?P<value>[\w\W\d]+)", authorization)
        if not value:
            raise BadRequestException("Invalid Authorization header")
        value = value.group(1)
        value = base64.b64decode(value).decode()
        username, password = tuple(value.split(":"))
        pre_response = self.validation(username, password)
        func_kwargs[headers_param_name] = pre_response
        return pre_response


class Pipe:
    def __init__(self, name, pipe_cls: PipeTransform) -> None:
        self.name = name
        self.pipe_cls = pipe_cls

    def __call__(self, func):
        key = get_func_key(func)
        if key not in pipes_map:
            pipes_map[key] = []
        pipes_map[key].append({"name": self.name, "pipe_cls": self.pipe_cls})
        return func


class Query:
    def __init__(
        self,
        name,
    ):
        self.name = name

    def __call__(self, func):
        # print("Query", func)
        key = f"{func.__module__}.{str(func.__qualname__)}"
        if key not in queries_map:
            queries_map[key] = []
        queries_map[key].append(
            {
                "name": self.name,
            }
        )
        return func


class Body:
    def __init__(
        self,
        name,
    ):
        self.name = name

    def __call__(self, func):
        # logger.log(DEBUG, f"Add to body: {func}")
        key = get_func_key(func)
        if key not in bodies_map:
            bodies_map[key] = {
                "name": self.name,
            }
        else:
            nestpy_logger.log(DEBUG, "Body decorator already defined")
        return func


class Dto:
    def __call__(self, cls):
        data_transfer_objs[get_class_key(cls)] = cls
        return cls


class ControllerKwargs(TypedDict, total=False):
    name: str
    version: str
    path: str


class Controller:
    def __init__(self, *args: Union[str, Dict[str, Any]], **kwargs: ControllerKwargs):
        self.name = None
        self.version = None
        self.bad_arguments = None
        if len(args) == 1 and isinstance(args[0], str):
            self.name = args[0]
            return

        if len(args) == 1 and isinstance(args[0], dict):
            self.name = None
            self.version = args[0]["version"] if "version" in args[0] else ""
            return

        if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], dict):
            self.name = args[0]
            self.version = args[1]["version"] if "version" in args[1] else ""
            return

        if len(kwargs) > 0:
            self.name = kwargs.get("name") or kwargs.get("path")
            self.version = kwargs.get("version")
            return

        if len(args):
            self.bad_arguments = True

    def __call__(self, clazz):
        if not "Nestpy" in ready:
            return
        if not self.name:
            self.name = str(clazz.__name__).lower()
        controllers.append({"class": clazz, "name": self.name, "version": self.version})
        if self.bad_arguments:
            nestpy_logger.warning(
                f"Bad arguments for controller decorator: {clazz.__name__}"
            )


def Injectable(cls):
    if not "Nestpy" in ready:
        return cls
    key = get_class_key(cls)
    nestpy_logger.info(
        f"Load injectable: {Fore.BLUE}{key}{Fore.RESET} - {cls.__name__}"
    )
    if key in injectables and injectables[key]["instance"]:
        return cls

    injectables[key] = {"class": cls, "instance": None}
    return cls


class MethodDecorator:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        key = f"{func.__module__}.{str(func.__qualname__).split('.')[0]}"
        if key not in methods_map:
            methods_map[key] = []
        methods_map[key].append(
            {
                "method": self.get_method(),
                "args": self.args,
                "kwargs": self.kwargs,
                "func": func,
            }
        )
        return func

    @abstractmethod
    def get_method(self) -> str:
        """Not implemented yet"""


class Get(MethodDecorator):
    def get_method(self) -> str:
        return "GET"


class Post(MethodDecorator):
    def get_method(self) -> str:
        return "POST"


class Put(MethodDecorator):
    def get_method(self) -> str:
        return "PUT"


class Delete(MethodDecorator):
    def get_method(self) -> str:
        return "DELETE"


class Options(MethodDecorator):
    def get_method(self) -> str:
        return "OPTIONS"


class Patch(MethodDecorator):
    def get_method(self) -> str:
        return "PATCH"


class Head(MethodDecorator):
    def get_method(self) -> str:
        return "HEAD"
