from typing import List


class RootException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return f"ActionMapper.{self.__class__.__name__}: {self.message}"

    def __repr__(self):
        return f"ActionMapper.{self.__class__.__name__}: {self.message}"


class ImplemenationException(RootException):
    ...


class TypeMismatchException(ImplemenationException):
    ...


class ActionException(RootException):
    def __init__(self, message: str, status_code: int, error_code: str, context=None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = message
        self.context = context


class ValidationException(RootException):
    def __init__(self, message: str, errors: List[str]):
        super().__init__(message)
        self.errors = errors


class IncomingDataSchemaInvalid(ValidationException):
    ...


class ActionInputSchemaInvalid(ValidationException):
    ...

