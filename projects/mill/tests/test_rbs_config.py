from unittest.mock import MagicMock, mock_open, patch

from mill.config import make_mill_config
import tomli


@patch('builtins.open', mock_open(read_data="data"))
def test_make_mill_config():
    tomli.load = MagicMock(return_value={
        'erd': {
            'drivers': {
                'mdrive_z': {'title': "MDrive Z", 'type': 'mdrive', 'url': 'some_url'},
                'mdrive_theta': {'title': "MDrive Theta", 'type': 'mdrive', 'url': 'some_url'},
                'mpa3': {'title': "mpa3", 'type': 'mdrive', 'url': 'some_url'},
            },
            'local_dir': '/tmp/data/',
            'remote_dir': '/tmp/REM/data'},
        'rbs': {
            'drivers': {
                'aml_x_y': {"type": "aml", "url": "some_url", "names": ["x", "y"], "title": "AML X Y"},
                'aml_phi_zeta': {"type": "aml", "url": "some_url", "names": ["phi", "zeta"], "title": "AML Phi Zeta"},
                'aml_det_theta': {"type": "aml", "url": "some_url", "names": ["det", "theta"],
                                  "title": "AML Det Theta"},
                'caen': {"type": "caen", "url": "some_url", "title": "Caen", "detectors": []},
                'motrona_charge': {"type": "motrona_dx350", "url": "some_url", "title": "Motrona Charge"}
            },
            'local_dir': '/tmp/data/',
            'remote_dir': '/tmp/REM/data'}
    })

    mill_config = make_mill_config("")

    assert (mill_config.rbs.drivers.aml_x_y.title == "AML X Y")
    assert (mill_config.rbs.drivers.aml_det_theta.title == "AML Det Theta")
    assert (mill_config.rbs.drivers.aml_phi_zeta.title == "AML Phi Zeta")
    assert (mill_config.rbs.drivers.motrona_charge.title == "Motrona Charge")
    assert (mill_config.rbs.drivers.caen.title == "Caen")
