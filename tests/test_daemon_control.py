import pytest
from unittest.mock import AsyncMock
from unittest.mock import call

import app.rbs_experiment.entities as rbs
import app.rbs_experiment.daemon_control as control

control.daemons.aml_x_y.url = "url_x_y"
control.daemons.aml_phi_zeta.url = "url_phi_zeta"
control.daemons.aml_det_theta.url = "url_det_theta"
control.daemons.caen_rbs.url = "url_caen_rbs"
control.daemons.motrona_rbs.url = "url_motrona_rbs"


@pytest.mark.asyncio
async def test_move_to_x_position():
    position = rbs.PositionCoordinates(x=5)
    control.comm = AsyncMock()
    await control.move_to_position("move", position)
    control.comm.move_aml_first.assert_called_with("move_first", "url_x_y", 5)
    control.comm.move_aml_second.assert_not_called()


@pytest.mark.asyncio
async def test_move_to_y_position():
    position = rbs.PositionCoordinates(y=10)
    control.comm = AsyncMock()
    await control.move_to_position("move", position)
    control.comm.move_aml_second.assert_called_with("move_second", "url_x_y", 10)
    control.comm.move_aml_first.assert_not_called()


@pytest.mark.asyncio
async def test_move_to_full_position():
    position = rbs.PositionCoordinates(x=1, y=2, phi=3, zeta=4, detector=5, theta=6)
    control.comm = AsyncMock()
    await control.move_to_position("move", position)

    control.comm.move_aml_first.assert_has_calls([call("move_first", "url_x_y", 1),
                                                  call("move_first", "url_phi_zeta", 3),
                                                  call("move_first", "url_det_theta", 5)])

    control.comm.move_aml_second.assert_has_calls([call("move_second", "url_x_y", 2),
                                                   call("move_second", "url_phi_zeta", 4),
                                                   call("move_second", "url_det_theta", 6)])


@pytest.mark.asyncio
async def test_move_to_none():
    position = rbs.PositionCoordinates()
    control.comm = AsyncMock()
    await control.move_to_position("move", position)
    control.comm.move_aml_second.assert_not_called()
    control.comm.move_aml_first.assert_not_called()


@pytest.mark.asyncio
async def test_move_to_angle_phi_2_5():
    control.comm = AsyncMock()
    await control.move_to_angle("move", rbs.CoordinateEnum.phi, 2.5)
    control.comm.move_aml_first.assert_called_with("move_first", "url_phi_zeta", 2.5)


@pytest.mark.asyncio
async def test_move_to_angle_zeta_3_5():
    control.comm = AsyncMock()
    await control.move_to_angle("move", rbs.CoordinateEnum.zeta, 3.5)
    control.comm.move_aml_second.assert_called_with("move_second", "url_phi_zeta", 3.5)


@pytest.mark.asyncio
async def test_move_to_angle_theta_4_5():
    control.comm = AsyncMock()
    await control.move_to_angle("move", rbs.CoordinateEnum.theta, 4.5)
    control.comm.move_aml_second.assert_called_with("move_second", "url_det_theta", 4.5)


@pytest.mark.asyncio
async def test_move_to_angle_and_acquire():
    control.comm = AsyncMock()
    control.move_to_angle = AsyncMock()
    await control.move_angle_and_count("step_1", rbs.CoordinateEnum.theta, 2.0)
    control.move_to_angle.assert_called_with("step_1", rbs.CoordinateEnum.theta, 2.0)
    control.comm.clear_and_arm_caen_acquisition.assert_called_with("step_1", "url_caen_rbs")
    control.comm.clear_start_motrona_count.assert_called_with("step_1", "url_motrona_rbs")
    control.comm.motrona_counting_done("step_1", "url_motrona_rbs")


