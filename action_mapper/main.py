import cerberus
from typing import List, Dict, Tuple, Any, Callable, Union, Type
from action_mapper import custom_types, exceptions

custom_types.Validator.register(cerberus.Validator)


class ActionMapperMixin:
    action: Callable = None
    action_input_schema: Dict = None
    data_input_schema: Dict = None
    fold_errors_to_error = True
    validator: Type[custom_types.Validator] = cerberus.Validator
    _action_input_schema = None
    _data_input_schema = None
    
    @classmethod
    def if_not_create_schemas(cls):
        if cls._action_input_schema is None:
            cls._action_input_schema = cls.validator(cls.action_input_schema)
        if cls._data_input_schema is None:
            cls._data_input_schema = cls.validator(cls.data_input_schema)

    @staticmethod
    def validate(validator: custom_types.Validator, data: Any) -> Tuple[bool, custom_types.ERRORS]:
        """
        return True if data is validated else False, Errors

        :param validator:
        :param data:
        :return:
        """
        if not isinstance(validator, custom_types.Validator):
            raise exceptions.TypeMismatchException("validator instance must implement Validator interface")

        is_valid: bool = validator.validate(data)
        validation_errors: List[str] = []

        if isinstance(validator, cerberus.Validator):
            if not is_valid:
                errors_: Dict = validator.errors  # {'field' : [error: str], .. }
                for field, errors in errors_.items():
                    errors = [] if errors is None else errors
                    validation_error = f'"{field}" - {",".join(errors)}'
                    validation_errors.append(validation_error)
        return is_valid, validation_errors

    def run_action(self):
        try:
            result = self.action(**self.get_action_arguments())
            return self.get_success_response(result)
        except exceptions.ActionException as e:
            return self.get_error_response(e)

    def set_action_arguments(self, action_arguments):
        self._action_arguments = action_arguments

    def get_action_arguments(self) -> dict:
        return self._action_arguments

    @staticmethod
    def get_success_response(action_result: Any) -> dict:
        return {
            'success': True,
            'result': action_result
        }

    @staticmethod
    def get_error_response(e: exceptions.ActionException) -> dict:
        return {
            'success': False,
            'result': e
        }

    def map_incoming_to_action(self, in_data: dict, *args, **kwargs):
        raise NotImplementedError()

    def map_action_output_to_response(
            self,
            is_success: bool,
            result: Any,
            exception: exceptions.ActionException=None
    ) -> Union[Dict, List]:
        raise NotImplementedError()

    def run(self, incoming_data, *args, **kwargs) -> Union[Dict, List]:
        self.if_not_create_schemas()
        is_input_valid, errors = self.validate(self._data_input_schema, incoming_data)
        if not is_input_valid:
            raise exceptions.IncomingDataSchemaInvalid(errors=errors, message='invalid incoming data')
        action_arguments = self.map_incoming_to_action(incoming_data, *args, **kwargs)
        is_action_input_valid, errors = self.validate(self._action_input_schema, action_arguments)
        if not is_action_input_valid:
            raise exceptions.ActionInputSchemaInvalid(errors=errors, message='invalid input to action')
        self.set_action_arguments(action_arguments)
        action_result = self.run_action()
        response = self.map_action_output_to_response(
            is_success=action_result["success"],
            result=None if not action_result["success"] else action_result["result"],
            exception=None if action_result["success"] else action_result["result"],
        )
        return response
