from pathlib import Path

from waspy.drivers.http_helper import get_json_safe
from waspy.iba.erd_entities import ErdDriverUrls, ErdRecipe
from waspy.iba.erd_recipes import run_erd_recipe, save_erd_journal
from waspy.iba.erd_setup import ErdSetup
from waspy.iba.file_writer import FileWriter
from waspy.iba.rbs_entities import RbsRandom, PositionCoordinates, CoordinateRange, RbsDriverUrls, Detector, Window, \
    RbsChanneling
from waspy.iba.rbs_recipes import run_random, save_rbs_journal, run_channeling, save_channeling_journal
from waspy.iba.rbs_setup import RbsSetup
import logging

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d__%H:%M__%S')


def setup() -> RbsSetup:
    rbs_setup = RbsSetup(
        RbsDriverUrls(
            aml_x_y="http://localhost:20000/api/latest",
            aml_phi_zeta="http://localhost:20000/api/latest",
            aml_det_theta="http://localhost:20000/api/latest",
            motrona_charge="http://localhost:20100/api/latest",
            caen="http://localhost:20200/api/latest"
        )
    )
    rbs_setup.configure_detectors([
        Detector(identifier="d01", board="33", channel="0", bins_min=0, bins_max=11264, bins_width=1024),
        Detector(identifier="d02", board="33", channel="1", bins_min=0, bins_max=11264, bins_width=1024),
    ])
    rbs_setup.fake()
    return rbs_setup


def run_random_example():
    rbs_setup = setup()
    recipe = RbsRandom(type="rbs_random", sample="HS12_02", name="RBS22_082_01A", charge_total=45000,
                       start_position=PositionCoordinates(x=10, y=22, phi=0),
                       coordinate_range=CoordinateRange(name="phi", start=0, end=30, increment=2))
    journal = run_random(recipe, rbs_setup)
    file_writer = FileWriter(Path("./result/"))
    save_rbs_journal(file_writer, recipe, journal)


def run_channeling_example():
    rbs_setup = setup()
    recipe = RbsChanneling(
        type="rbs_channeling", sample="HS12_02", name="RBS22_082_01A",
        start_position=PositionCoordinates(x=10, y=22, phi=0),
        yield_charge_total=2000, yield_coordinate_ranges=[
            CoordinateRange(name="zeta", start=-2, end=2, increment=0.2),
            CoordinateRange(name="theta", start=-2, end=2, increment=0.2),
            CoordinateRange(name="zeta", start=-2, end=2, increment=0.2),
            CoordinateRange(name="theta", start=-2, end=2, increment=0.2)
        ],
        yield_integration_window=Window(start=550, end=650),
        yield_optimize_detector_identifier="d01", compare_charge_total=30000,
        random_coordinate_range=CoordinateRange(name="phi", start=0, end=30, increment=2)
    )

    journal = run_channeling(recipe, rbs_setup)
    file_writer = FileWriter(Path("./result/"))
    save_channeling_journal(file_writer, recipe, journal)


def run_erd_example():
    erd_setup = ErdSetup(ErdDriverUrls(
        mpa3="http://127.0.0.1:22400/api/latest",
        mdrive_z="http://127.0.0.1:22300/api/latest",
        mdrive_theta="http://127.0.0.1:22300/api/latest"
    ))
    erd_setup.fake()

    recipe = ErdRecipe(
        measuring_time_sec=3600, type="erd", sample="HS12_03", name="ERD22_082_01A",
        theta=50, z_start=20, z_end=30, z_increment=1, z_repeat=1
    )

    journal = run_erd_recipe(recipe, erd_setup)
    file_writer = FileWriter(Path("./result/"))
    save_erd_journal(file_writer, recipe, journal)


run_erd_example()
