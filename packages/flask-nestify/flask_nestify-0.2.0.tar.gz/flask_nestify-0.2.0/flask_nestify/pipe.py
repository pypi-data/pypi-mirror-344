import types
from abc import ABC, abstractmethod
from .utils import get_func_key
from .globals import pipes_map


class PipeTransform(ABC):
    @abstractmethod
    def transform(self, value):
        """Not implemented yet"""


class ParseInt(PipeTransform):
    def transform(self, value):
        if isinstance(value, str):
            return int(value)
        elif isinstance(value, int):
            return value
        else:
            raise Exception("Invalid type")


class PipeProcessor:
    def __init__(self, func: types.FunctionType) -> None:
        self.func = func
        self.key = get_func_key(self.func)
        self.pipes = []
        if self.key in pipes_map:
            self.pipes = pipes_map[self.key]

    def process(self, kwargs):
        for pipe in self.pipes:
            if pipe["name"] in kwargs:
                pipe_transform = pipe["pipe_cls"]()
                kwargs[pipe["name"]] = pipe_transform.transform(kwargs[pipe["name"]])
