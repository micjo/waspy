import unittest
from unittest.mock import MagicMock

import waspy.hardware_control.motrona_dx350
from waspy.hardware_control.motrona_dx350 import MotronaDx350


class TestDbTables(unittest.TestCase):
    def setUp(self):
        self.motrona_dx350 = MotronaDx350("http://localhost:22100")
        waspy.hardware_control.motrona_dx350.post_request = MagicMock()
        waspy.hardware_control.motrona_dx350.generate_request_id = MagicMock(return_value="some_request")

    def test_pause_counting(self):
        self.motrona_dx350.pause()
        waspy.hardware_control.motrona_dx350.generate_request_id.assert_called_once()
        waspy.hardware_control.motrona_dx350.post_request.assert_called_once_with("http://localhost:22100",
                                                                                  {"request_id": "some_request",
                                                                                   "pause_counting": True})

    def test_start_count_from_zero(self):
        self.motrona_dx350.start_count_from_zero()
        waspy.hardware_control.motrona_dx350.generate_request_id.assert_called_once()
        waspy.hardware_control.motrona_dx350.post_request.assert_called_once_with("http://localhost:22100",
                                                                                  {"request_id": "some_request",
                                                                                   "clear-start_counting": True})

    def test_start_count(self):
        self.motrona_dx350.start_count()
        waspy.hardware_control.motrona_dx350.generate_request_id.assert_called_once()
        waspy.hardware_control.motrona_dx350.post_request.assert_called_once_with("http://localhost:22100",
                                                                                  {"request_id": "some_request",
                                                                                   "start_counting": True})

    def test_set_target_charge(self):
        self.motrona_dx350.set_target_charge(500)
        waspy.hardware_control.motrona_dx350.generate_request_id.assert_called_once()
        waspy.hardware_control.motrona_dx350.post_request.assert_called_once_with("http://localhost:22100",
                                                                                  {"request_id": "some_request",
                                                                                   "target_charge": 500})

    def test_counting_done(self):
        waspy.hardware_control.motrona_dx350.get_json = MagicMock()
        waspy.hardware_control.motrona_dx350.sleep = MagicMock()
        waspy.hardware_control.motrona_dx350.get_json.side_effect = [
            {"status": "nope"},
            {"status": "nope"},
            {"status": "Done"}
        ]
        self.motrona_dx350.wait_for_counting_done()
        self.assertEqual(waspy.hardware_control.motrona_dx350.get_json.call_count, 3)

    def test_get_status(self):
        waspy.hardware_control.motrona_dx350.get_json = MagicMock(return_value={"dummy": "value"})
        status = self.motrona_dx350.get_status()
        self.assertEqual(status, {"dummy": "value"})
        waspy.hardware_control.motrona_dx350.get_json.assert_called_once()




