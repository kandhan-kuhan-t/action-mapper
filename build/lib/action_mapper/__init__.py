from . import custom_types, exceptions, adapters
from .main import ActionMapperMixin
import testutils
import cerberus
import unittest.mock


class ValidatorMockSubclass(cerberus.Validator):
    ...


custom_types.Validator.register(ValidatorMockSubclass)

ValidatorMock = unittest.mock.create_autospec(spec=ValidatorMockSubclass)


class TestCase(unittest.TestCase):
    def setUp(self):
        self.ds = testutils.DataStore()
        self.Validator = ValidatorMock






