import unittest
from unittest.mock import MagicMock

import waspy.hardware_control.aml
from waspy.hardware_control.aml import Aml


class TestDbTables(unittest.TestCase):
    def setUp(self):
        self.aml = Aml("http://localhost:22100")
        waspy.hardware_control.aml.post_request = MagicMock()
        waspy.hardware_control.aml.generate_request_id = MagicMock(return_value="some_request")

    def test_move_first(self):
        self.aml.move_first(5)
        waspy.hardware_control.aml.generate_request_id.assert_called_once()
        waspy.hardware_control.aml.post_request.assert_called_once_with("http://localhost:22100", {"request_id":"some_request", "set_m1_target_position": 5}, True)

    def test_move_second(self):
        self.aml.move_second(20)
        waspy.hardware_control.aml.generate_request_id.assert_called_once()
        waspy.hardware_control.aml.post_request.assert_called_once_with("http://localhost:22100", {"request_id":"some_request", "set_m2_target_position": 20}, True)

    def test_load(self):
        self.aml.load()
        waspy.hardware_control.aml.generate_request_id.assert_called_once()
        waspy.hardware_control.aml.post_request.assert_called_once_with("http://localhost:22100", {"request_id":"some_request","m1_load":True, "m2_load": True}, True)

    def test_get_status(self):
        waspy.hardware_control.aml.get_json = MagicMock(return_value={"dummy": "value"})
        status = self.aml.get_status()
        self.assertEqual(status, {"dummy": "value"})
        waspy.hardware_control.aml.get_json.assert_called_once()





