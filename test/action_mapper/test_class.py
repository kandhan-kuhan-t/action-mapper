from unittest import mock
import action_mapper
import testutils


class TestValidate(action_mapper.TestCase):
    def setUp(self):
        super().setUp()
        self.ac_map = action_mapper.ActionMapperMixin()
        self.ac_map.if_not_create_schemas = mock.MagicMock()
        self.ac_map.validate = mock.MagicMock()
        self.ac_map.validate.return_value = (True, [])
        self.ds = testutils.DataStore()

    def tearDown(self):
        ...

    def test_get_success_response(self):
        ...

    def test_get_error_response(self):
        ...

    # noinspection PyUnresolvedReferences
    def test_run_action_success_flow(self):
        self.ac_map.action = self.ds.magicmock_action
        self.ac_map.get_action_arguments = self.ds.magicmock_get_action_arguments
        self.ac_map.get_success_response = self.ds.magicmock_get_success_response
        self.ac_map.get_error_response = self.ds.magicmock_get_error_response

        self.ac_map.run_action()
        self.ac_map.action.assert_called_with(**self.ac_map.get_action_arguments.return_value)
        self.ac_map.get_success_response.assert_called_with(self.ac_map.action.return_value)
        self.ac_map.get_error_response.assert_not_called()

    # noinspection PyUnresolvedReferences
    def test_run_action_error_flow(self):
        self.ac_map.action = self.ds.magicmock_action
        self.action_exception = action_mapper.exceptions.ActionException(
            message=self.ds.str_message, status_code=self.ds.int_status_code, error_code=self.ds.str_error_code
        )
        self.ac_map.action.side_effect = self.action_exception
        self.ac_map.get_action_arguments = self.ds.magicmock_get_action_arguments
        self.ac_map.get_success_response = self.ds.magicmock_get_success_response
        self.ac_map.get_error_response = self.ds.magicmock_get_error_response

        self.ac_map.run_action()
        self.ac_map.action.assert_called_with(**self.ac_map.get_action_arguments.return_value)
        self.ac_map.get_success_response.assert_not_called()
        self.ac_map.get_error_response.assert_called_with(self.action_exception)

    # noinspection PyUnresolvedReferences
    def test_run_success(self):
        self.ac_map.map_incoming_to_action = self.ds.magicmock_map_incoming_to_action
        self.ac_map.set_action_arguments = self.ds.magicmock_set_action_arguments
        self.ac_map.run_action = self.ds.magicmock_run_action
        self.ac_map.run_action.return_value = {
            "is_success": True,
            "result": self.ds.magicmock_result
        }
        self.ac_map.map_action_output_to_response = self.ds.magicmock_map_action_output_to_response
        self.assertEqual(
            self.ac_map.run(self.ds.magicmock_incoming_data),
            self.ac_map.map_action_output_to_response.return_value
        )
        self.ac_map.map_incoming_to_action.assert_called_with(self.ds.magicmock_incoming_data)
        self.ac_map.set_action_arguments.assert_called_with(self.ac_map.map_incoming_to_action.return_value)
        self.ac_map.run_action.assert_called_once()
        self.ac_map.map_action_output_to_response.assert_called_with(
            is_success=True,
            result=self.ds.magicmock_result,
            exception=None
        )

    # noinspection PyUnresolvedReferences
    def test_run_fail(self):
        self.ac_map.map_incoming_to_action = self.ds.magicmock_map_incoming_to_action
        self.ac_map.set_action_arguments = self.ds.magicmock_set_action_arguments
        self.ac_map.run_action = self.ds.magicmock_run_action
        self.ac_map.run_action.return_value = {
            "is_success": False,
            "result": self.ds.magicmock_result
        }
        self.ac_map.map_action_output_to_response = self.ds.magicmock_map_action_output_to_response
        self.assertEqual(
            self.ac_map.run(self.ds.magicmock_incoming_data),
            self.ac_map.map_action_output_to_response.return_value
        )
        self.ac_map.map_incoming_to_action.assert_called_with(self.ds.magicmock_incoming_data)
        self.ac_map.set_action_arguments.assert_called_with(self.ac_map.map_incoming_to_action.return_value)
        self.ac_map.run_action.assert_called_once()
        self.ac_map.map_action_output_to_response.assert_called_with(
            is_success=False,
            result=None,
            exception=self.ds.magicmock_result,
        )
