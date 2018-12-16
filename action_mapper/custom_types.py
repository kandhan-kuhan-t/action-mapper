from typing import List, Any
import abc

ERRORS = List[str]


# noinspection PyPropertyDefinition
class Validator(abc.ABC):
    def __init__(self, *args, **kwargs): ...

    def validate(self, data) -> bool: ...

    @property
    def errors(self) -> Any: ...
