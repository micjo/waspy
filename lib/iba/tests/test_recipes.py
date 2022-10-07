import tempfile
import unittest

from waspy.iba.file_writer import FileWriter
from waspy.iba.rbs_entities import RbsChanneling, RecipeType, CoordinateRange, Window, RbsDriverUrls, HardwareUrl, \
    Detector, RbsRandom
from waspy.iba.rbs_recipes import run_channeling, run_random
from waspy.iba.rbs_setup import RbsSetup
from unittest.mock import Mock
import logging

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d__%H:%M__%S')



class TestRecipes(unittest.TestCase):
    def setUp(self):
        self.rbs = RbsSetup(RbsDriverUrls(
            aml_x_y=HardwareUrl(url="http://127.0.0.1:20000/api/latest"),
            aml_phi_zeta=HardwareUrl(url="http://127.0.0.1:20000/api/latest"),
            aml_det_theta=HardwareUrl(url="http://127.0.0.1:20000/api/latest"),
            caen=HardwareUrl(url="http://127.0.0.1:20200/api/latest"),
            motrona_charge=HardwareUrl(url="http://127.0.0.1:20100/api/latest"),
        ))

        d01 = Detector(board="33", channel=0, identifier="d01", bins_min=0, bins_max=11264, bins_width=1024)
        d02 = Detector(board="33", channel=0, identifier="d02", bins_min=0, bins_max=11264, bins_width=1024)
        md01 = Detector(board="33", channel=0, identifier="md01", bins_min=0, bins_max=11264, bins_width=1024)
        md02 = Detector(board="33", channel=0, identifier="md02", bins_min=0, bins_max=11264, bins_width=1024)
        self.rbs.configure_detectors([d01, d02, md01, md02])
        self.rbs.fake()

        # TODO: dependency on file system in tests -> BAD. need to return text from code and test the text
        self.file_writer = Mock(spec=FileWriter)

    def test_random(self):
        recipe = RbsRandom(
            type=RecipeType.RANDOM, sample="sample_001", name="recipe_001",
            charge_total=50000, coordinate_range=CoordinateRange(start=0, end=30, increment=2, name="phi")
        )
        run_random(recipe, self.rbs, self.file_writer, {})

    def test_channeling(self):
        recipe = RbsChanneling(
            type=RecipeType.CHANNELING, sample="sample_001", name="recipe_001",
            yield_charge_total=5000, yield_coordinate_ranges=
            [
                CoordinateRange(start=-2, end=2, increment=0.2, name="zeta"),
                CoordinateRange(start=-2, end=2, increment=0.2, name="theta"),
                CoordinateRange(start=-2, end=2, increment=0.2, name="zeta"),
                CoordinateRange(start=-2, end=2, increment=0.2, name="theta"),
            ],
            yield_integration_window=Window(start=550, end=650),
            yield_optimize_detector_identifier="d01",
            compare_charge_total=60000,
            random_coordinate_range=CoordinateRange(start=0, end=30, increment=0.2, name="phi")
        )

        run_channeling(recipe, self.rbs, self.file_writer, {})
