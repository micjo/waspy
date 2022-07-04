import unittest
from unittest.mock import MagicMock, create_autospec, Mock, call

from hive.rbs_data_serializer import RbsDataSerializer
from hive.rbs_job import RbsJob
from hive.rbs_entities import RbsJobModel
from waspy.hardware_control.rbs_entities import PositionCoordinates
from waspy.hardware_control.rbs_setup import RbsSetup


class TestDbTables(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run_random(self):
        job = RbsJobModel.parse_obj({
            "name": "RBS21_071", "type": "rbs",
            "recipes": [
                {"type": "rbs_stepwise", "sample": "AE007607_D02_A", "name": "RBS21_071_01B_A",
                 "start_position": {"x": 10, "y": 22, "phi": 0}, "charge_total": 45000,
                 "vary_coordinate": {"name": "phi", "start": 0, "end": 30, "increment": 2}
                 }
            ]
        }
        )
        rbs_setup = Mock(spec=RbsSetup)
        data_serializer = Mock(spec=RbsDataSerializer)
        job = RbsJob(job, rbs_setup, data_serializer)
        job.execute()

        move_calls = [call.move_and_count(PositionCoordinates(phi=pos)) for pos in range(0, 31, 2)]

        print(rbs_setup.mock_calls)

        call_list = [call.move(PositionCoordinates(x=10, y=22, phi=0)),
                     call.prepare_counting_with_target(45000 / 16),
                     call.start_data_acquisition()]
        call_list.extend(move_calls)
        call_list.extend([
            call.stop_data_acquisition(),
            call.get_status(True),
            call.get_corrected_total_accumulated_charge(),
            call.finish()
        ])

        rbs_setup.assert_has_calls(call_list)
