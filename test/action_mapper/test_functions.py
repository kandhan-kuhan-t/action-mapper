import action_mapper


class TestValidate(action_mapper.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        ...

    def test_validator_type_is_valid(self):

        # noinspection PyTypeChecker
        action_mapper.ActionMapperMixin.validate(validator=self.Validator(), data=self.ds.str)

    def test_calls_for_cerebrus_validator(self):
        validator = self.Validator()
        # noinspection PyTypeChecker
        action_mapper.ActionMapperMixin.validate(validator=validator, data=self.ds.str_data)
        validator.validate.assert_called_with(self.ds.str_data)
    
    def test_validation_errors_for_cerebrus(self):
        self.Validator.validate.return_value = False
        self.Validator.errors = {
            self.ds.str_key: [self.ds.str_error]
        }
        validator = self.Validator
        
        # noinspection PyTypeChecker
        is_valid, errors = action_mapper.ActionMapperMixin.validate(validator, data=self.ds.str)
        self.assertIsInstance(errors, list)
        self.assertEqual(len(errors), 1)
        self.assertListEqual(errors, [f'"{self.ds.str_key}" - {self.ds.str_error}'])
