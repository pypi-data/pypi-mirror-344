import os
import inspect
from typing import Union
from pathlib import Path
from typing import Tuple


def build_dto(data_transfer_objs: dict, data: dict, cls):
    cls_key = get_class_key(cls)
    if cls_key in data_transfer_objs:
        try:
            args = get_class_arguments(cls)
            kwargs = {}
            for arg in args:
                arg_name = arg[0]
                arg_cls = arg[1]
                arg_cls_key = get_class_key(arg_cls)
                if arg_name in data:
                    kwargs[arg_name] = (
                        build_dto(data_transfer_objs, data[arg_name], arg_cls)
                        if arg_cls_key in data_transfer_objs
                        else get_native_value(arg_cls, data[arg_name])
                    )
            return cls(**kwargs)
        except Exception as e:
            raise Exception(f"Error building DTO {e}")
    else:
        raise Exception("Parameter no register like DTO")


from typing import get_origin, get_args


def get_native_value(cls, value: any):
    # Resoluelve `Optional` para obtener el tipo subyacente
    if get_origin(cls) is Union:
        args = get_args(cls)
        # Verifica si es `Optional` (NoneType es parte del Union)
        if type(None) in args and len(args) == 2:
            cls = args[0] if args[1] is type(None) else args[1]

    if cls is int:
        return int(value)
    elif cls is float:
        return float(value)
    elif cls is str:
        return str(value)
    elif cls is dict:
        return dict(value)
    elif cls is list:
        return list(value)
    elif cls is bool:
        return value if isinstance(value, bool) else (str(value) in ["True", "true"])
    else:
        raise Exception("Unimplemented type yet")


def dict_2_obj(data: dict, cls):
    args = get_class_arguments(cls)
    kwargs = {}
    for arg in args:
        arg_name = arg[0]
        arg_cls = arg[1]
        if arg_name in data:
            kwargs[arg_name] = get_native_value(arg_cls, data[arg_name])
    return cls(**kwargs)


def get_class_key(cls):
    try:
        module_file = inspect.getfile(cls)
    except TypeError:
        module_file = "builtin"

    base_path = os.getcwd()
    if module_file != "builtin":
        if os.path.exists(module_file):
            module_file = os.path.relpath(module_file, base_path)
        module_path = ".".join(Path(module_file).with_suffix("").parts)
    else:
        module_path = cls.__module__
        if os.path.exists(module_path):
            module_path = os.path.relpath(module_path, base_path)
            module_path = ".".join(Path(module_path).with_suffix("").parts)

    name = cls.__qualname__
    return f"{module_path}.{name}"


def get_doc_file(func) -> Tuple[Path, Path]:
    base_path = os.getcwd()
    module = func.__module__
    if os.path.exists(module):
        module = os.path.relpath(module, base_path)
        doc_file = (
            Path(base_path)
            / Path("doc")
            / Path(module).with_suffix("")
            / Path(func.__name__)
        )
        return (doc_file.with_suffix(".yml"), doc_file.with_suffix(".yaml"))
    return None, None


def get_class_arguments(cls):
    args = []
    signatures = inspect.signature(cls.__init__)
    for sig in signatures.parameters:
        if not str(sig) in ["self", "args", "kwargs"]:
            param_name = str(sig)
            parameter = signatures.parameters[param_name]
            default = (
                parameter.default if parameter.default != parameter.empty else None
            )
            args.append((param_name, parameter.annotation, default))
    return args


def get_func_key(func):
    return f"{func.__module__}.{str(func.__qualname__)}"
