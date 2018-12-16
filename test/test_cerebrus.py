import unittest
import testutils
import cerberus


class TestCerberusInterface(unittest.TestCase):
    def setUp(self):
        self.schema = {
            'name': {'type': 'string', 'required': True}
        }
        self.validator = cerberus.Validator(self.schema)
        self.ds = testutils.DataStore()

    def test_is_valid(self):
        data = {
            'name': self.ds.str_name
        }
        self.assertTrue(self.validator.validate(data))

    def test_is_not_valid(self):
        data = {
            'name': self.ds.int
        }
        self.assertIsNotNone(self.validator.validate(data))

    def test_errors(self):
        data = {
        }
        self.validator.validate(data)
        errors = self.validator.errors
        self.assertIsNotNone(errors)
        self.assertIsInstance(errors, dict)
        self.assertEqual(len(errors), 1)
