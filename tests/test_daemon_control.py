from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import ANY

import projects.hive.src.hive.entities as entities

from projects.hive.src.hive.rbs_entities import RbsConfig, AmlConfig, SimpleConfig
from waspy.hardware_control import rbs_setup as rbs_lib
from waspy.hardware_control.rbs_entities import PositionCoordinates
import waspy.hardware_control.hw_action as hw_action


config = RbsConfig(
    aml_x_y=AmlConfig(type="aml", title="aml x y", url="url_x_y", key="aml_x_y",
                                                         names=["x", "y"], loads=[5, 10]),
    aml_phi_zeta=AmlConfig(type="aml", title="aml phi zeta", url="url_phi_zeta", key="aml_phi_zeta",
                                                              names=["phi", "zeta"], loads=[5, 10]),
    aml_det_theta=AmlConfig(type="aml", title="aml det theta", url="url_det_theta", key="aml_det_theta",
                                                               names=["det", "theta"], loads=[5, 10]),
    caen=SimpleConfig(type="caen", title="caen", url="url_caen", key="caen"),
    motrona=SimpleConfig(type="motrona", title="motrona", url="url_motrona", key="motrona")

)

rbs = rbs_lib.RbsSetup(config)


def test_move_to_x_position():
    position = PositionCoordinates(x=5)
    rbs_lib.hw_action = MagicMock()
    rbs.move(position)
    hw_action.move_aml_first.assert_called_with(ANY, "url_x_y", 5)
    hw_action.move_aml_second.assert_not_called()


def test_move_to_y_position():
    position = PositionCoordinates(y=10)
    rbs_lib.hw_action = MagicMock()
    rbs.move(position)
    hw_action.move_aml_second.assert_called_with(ANY, "url_x_y", 10)
    hw_action.move_aml_first.assert_not_called()


def test_move_to_full_position():
    position = PositionCoordinates(x=1, y=2, phi=3, zeta=4, detector=5, theta=6)
    rbs_lib.hw_action = MagicMock()
    rbs.move(position)

    hw_action.move_aml_first.assert_has_calls([call(ANY, "url_x_y", 1),
                                               call(ANY, "url_phi_zeta", 3),
                                               call(ANY, "url_det_theta", 5)])

    hw_action.move_aml_second.assert_has_calls([call(ANY, "url_x_y", 2),
                                                call(ANY, "url_phi_zeta", 4),
                                                call(ANY, "url_det_theta", 6)])


def test_move_to_none():
    position = waspy.hardware_control.rbs_entities.PositionCoordinates()
    rbs_lib.hw_action = MagicMock()
    rbs.move(position)
    hw_action.move_aml_second.assert_not_called()
    hw_action.move_aml_first.assert_not_called()


def test_move_to_angle_phi_2_5():
    rbs_lib.hw_action = MagicMock()
    target = PositionCoordinates(phi=2.5)
    rbs.move_and_count(target, lambda cb: None)
    hw_action.move_aml_first.assert_called_with(ANY, "url_phi_zeta", 2.5)
    hw_action.clear_start_motrona_count.assert_called_with(ANY, "url_motrona")
    hw_action.motrona_counting_done(ANY, "url_motrona")


def test_move_to_angle_zeta_3_5():
    rbs_lib.hw_action = MagicMock()
    rbs.move(PositionCoordinates(zeta=3.5))
    hw_action.move_aml_second.assert_called_with(ANY, "url_phi_zeta", 3.5)


def test_move_to_angle_theta_4_5():
    rbs_lib.hw_action = MagicMock()
    rbs.move(PositionCoordinates(theta=4.5))
    hw_action.move_aml_second.assert_called_with(ANY, "url_det_theta", 4.5)


def test_move_and_count():
    rbs_lib.hw_action = MagicMock()
    rbs.move_and_count(PositionCoordinates(theta=2.0), lambda cb: None)
    hw_action.move_aml_second.assert_called_with(ANY, "url_det_theta", 2.0)
    hw_action.clear_start_motrona_count.assert_called_with(ANY, "url_motrona")
    hw_action.motrona_counting_done(ANY, "url_motrona")


def test_entities():
    rbs_settings = entities.RbsRqmSettings(rqm_number="RBS21_232", detectors=[])
    assert rbs_settings.name == rbs_settings.base_folder
