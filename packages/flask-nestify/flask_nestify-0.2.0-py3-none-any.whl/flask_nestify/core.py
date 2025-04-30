import os
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from flask import Blueprint, Flask
from flasgger import swag_from
import flask

from .logger import nestpy_logger
from .exception import (
    NestpyException,
    nestpy_exception_handler,
)
from .body import BodyProcessor
from .decorator import Decorator
from .headers import HeadersProcessor
from .httpcode import HttpCodeProcessor
from .pipe import PipeProcessor
from .response import DefaultResponse, ResponseProcessor
from .query import QueryProcessor
from .utils import (
    get_class_arguments,
    get_class_key,
    get_doc_file,
    get_func_key,
)
from .globals import controllers
from .globals import injectables
from .globals import methods_map
from .globals import decorators
from .globals import ready


def binding(cls) -> object:
    arguments = get_class_arguments(cls)
    kwargs = {}
    for arg in arguments:
        arg_name = arg[0]
        arg_cls = arg[1]
        arg_value = arg[2]
        key = get_class_key(arg_cls)
        if key not in injectables and arg_value is None:
            nestpy_logger.error(f"Unable to build {cls.__name__}")
            return None

        if arg_value is not None:
            kwargs[arg_name] = arg_value
            continue

        injectable = injectables[key]
        instance = injectable["instance"]
        if instance:
            nestpy_logger.debug(f"Inject already exists {key} {instance}")
            kwargs[arg_name] = instance
        else:
            injectable_class = injectable["class"]
            argument_obj = binding(injectable_class)
            injectables[key]["instance"] = argument_obj
            kwargs[arg_name] = argument_obj
    return cls(**kwargs)


class Swaggerify:
    def __init__(self, doc=None, spec_dict=None) -> None:
        self.doc = doc
        self.spec_dict = spec_dict
        pass

    def __call__(self, func):
        func.__doc__ = self.doc
        func.specs_dict = self.spec_dict
        return func


class WrapperFunc:
    def __init__(self, object, func):
        self.object = object
        self.func = func
        self.func_key = get_func_key(func)
        self.query_proc = QueryProcessor(self.func)
        self.body_proc = BodyProcessor(self.func)
        self.pipe_proc = PipeProcessor(self.func)
        self.headers_proc = HeadersProcessor(self.func)
        self.response_proc = ResponseProcessor(self.func)
        self.http_code_proc = HttpCodeProcessor(self.func)
        self.decorators = (
            decorators[self.func_key] if self.func_key in decorators else []
        )
        self.func_doc_ = func.__doc__

    def wrapper_func(self):
        spec = None
        yml_file, yaml_file = get_doc_file(self.func)
        if yml_file and yml_file.exists():
            spec = str(yml_file)
        elif yaml_file and yaml_file.exists():
            spec = str(yaml_file)

        @swag_from(spec)
        @Swaggerify(doc=self.func.__doc__, spec_dict=None)
        def wrapper(*args, **kwargs):
            response = flask.Response()
            self.query_proc.process(kwargs)
            self.pipe_proc.process(kwargs)
            self.body_proc.process(kwargs)
            self.headers_proc.process(kwargs)
            self.response_proc.process(kwargs, response)

            for decorator in self.decorators:
                dec: Decorator = decorator["decorator"]
                pre_response = dec.pre_response(kwargs)
                if isinstance(pre_response, flask.Response):
                    return pre_response

            func_response = self.func(self.object, **kwargs)

            defResponse = DefaultResponse()
            self.http_code_proc.process(kwargs, response)

            for decorator in self.decorators:
                dec: Decorator = decorator["decorator"]
                dec.post_response(response)

            return defResponse.get_response(response, func_response)

        return wrapper


def Nestpy(flask_app: Flask):
    ready["Nestpy"] = True
    flask_app.url_map.strict_slashes = False
    flask_app.errorhandler(NestpyException)(nestpy_exception_handler)
    cwd = Path(os.getcwd())
    nestpy_logger.info("Start nestpy")

    for service in cwd.rglob("*_service.py"):
        if service.name.startswith("test_"):
            continue
        lib = spec_from_file_location(str(service), str(service))
        mod = module_from_spec(lib)
        lib.loader.exec_module(mod)

    for controller in cwd.rglob("*_controller.py"):
        if controller.name.startswith("test_"):
            continue
        lib = spec_from_file_location(str(controller), str(controller))
        mod = module_from_spec(lib)
        lib.loader.exec_module(mod)

    # for models in cwd.rglob("*_model.py"):
    #     try:
    #         if models.name.startswith("test_"):
    #             continue
    #         lib = spec_from_file_location(str(models), str(models))
    #         mod = module_from_spec(lib)
    #         lib.loader.exec_module(mod)
    #     except InvalidRequestError:
    #         nestpy_logger.debug("Model already exists %s", models)
    #     except (ImportError, AttributeError, FileNotFoundError) as e:
    #         nestpy_logger.error("Error loading model %s %s", models, e)

    for controller in controllers:
        register_controller(flask_app, controller)


def register_controller(flask_app, controller):
    cls = controller["class"]
    controller_name = controller["name"]
    controller_version = controller["version"]
    # print(controller)
    nestpy_logger.info(f"Controller {cls.__name__}")

    obj = binding(cls)

    # print("Create object", obj)
    key = f"{cls.__module__}.{str(cls.__qualname__).split('.')[0]}"
    # print(key)

    blueprint = Blueprint(f"bp_{controller_name}", cls.__name__)
    # print("Controller name:", controller_name)

    version = (f"/{controller_version}") if controller_version else ""
    url_prefix = f"{version}/{controller_name}"

    if key in methods_map:
        methods: list = methods_map[key]
        for method in methods:
            route = ("/" + method["args"][0]) if method["args"] else ""
            nestpy_logger.info_mapped(method["method"], f"{url_prefix}{route}")

            wrapper = WrapperFunc(obj, method["func"])

            bp_function = Blueprint(
                f"func_{controller_name}_{method['func'].__name__}",
                method["func"].__name__,
            )

            # f = swaggerify(wrapper.wrapper_func)

            # print("---", f)

            bp_function.route(route, methods=[method["method"]])(wrapper.wrapper_func())

            blueprint.register_blueprint(bp_function)

    flask_app.register_blueprint(blueprint, url_prefix=url_prefix)
