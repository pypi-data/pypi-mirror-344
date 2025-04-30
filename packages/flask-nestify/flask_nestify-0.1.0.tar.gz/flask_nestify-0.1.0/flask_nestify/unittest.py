from unittest.mock import MagicMock
from .utils import get_class_key
from .globals import injectables


class PatchService:

    def __init__(self, clz, attribute: str) -> None:
        self.clz = clz
        self.attribute = attribute

    def __enter__(self):
        self.mock = MagicMock()
        clz_key = get_class_key(self.clz)
        if not clz_key in injectables:
            raise Exception(f"Class {self.clz} not found in injectables")
        if (
            not "instance" in injectables[clz_key]
            or not injectables[clz_key]["instance"]
        ):
            raise Exception(f"Instance not found for class {self.clz} in injectables")
        instance = injectables[clz_key]["instance"]
        self.instance_value = getattr(instance, self.attribute)
        setattr(instance, self.attribute, self.mock)
        return self.mock

    def __exit__(self, exc_type, exc_value, traceback):
        clz_key = get_class_key(self.clz)
        instance = injectables[clz_key]["instance"]
        setattr(instance, self.attribute, self.instance_value)
        return self.mock.__exit__(exc_type, exc_value, traceback)
