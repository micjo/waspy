import pytest
import tomli

from app.setup.config import make_rbs_config, make_hardware_config


def test_make_rbs_config():
    config = {
        'generic': {'hardware': {
            'aml_x_y': {'type': 'aml', 'title': 'AML X Y', 'url': 'http://localhost:22000/api/latest',
                        'names': ['X', 'Y'], 'loads': [110, 20]},
            'aml_det_theta': {'type': 'aml', 'title': 'AML Detector Theta', 'url': 'http://localhost:22001/api/latest',
                              'names': ['Detector', 'Theta'], 'loads': [170, 10]},
            'aml_phi_zeta': {'type': 'aml', 'title': 'AML Phi Zeta', 'url': 'http://localhost:22002/api/latest',
                             'names': ['Phi', 'Zeta'], 'loads': [0, -1]},
            'motrona_rbs': {'type': 'motrona', 'title': 'Motrona RBS', 'url': 'http://localhost:22100/api/latest'},
            'caen_rbs': {'type': 'caen', 'title': 'Caen RBS', 'url': 'http://localhost:22200/api/latest'},
            'mdrive': {'type': 'mdrive', 'title': 'MDrive', 'url': 'http://localhost:22300/api/latest'}}},
        'erd': {'hardware': {'mdrive': 'mdrive'}},
        'rbs': {
            'hardware': {'aml_x_y': 'aml_x_y', 'aml_phi_zeta': 'aml_phi_zeta', 'aml_det_theta': 'aml_det_theta',
                         'caen': 'caen_rbs', 'motrona': 'motrona_rbs'}, 'input_dir': {'watch': '/tmp/ACQ/1_watch'},
            'output_dir': {'ongoing': '/tmp/ACQ/2_ongoing', 'done': '/tmp/ACQ/3_done', 'failed': '/tmp/ACQ/4_failed',
                           'data': '/tmp/ACQ/5_data'},
            'remote_output_dir': {'ongoing': '/tmp/ACQ/REM/_02_ongoing', 'done': '/tmp/ACQ/REM/_03_done',
                                  'failed': '/tmp/ACQ/REM/_04_failed', 'data': '/tmp/ACQ/REM/_05_data'}}}

    rbs = make_rbs_config(config)

    assert (rbs.aml_x_y.title == "AML X Y")
    assert (rbs.aml_det_theta.title == "AML Detector Theta")
    assert (rbs.aml_phi_zeta.title == "AML Phi Zeta")
    assert (rbs.motrona.title == "Motrona RBS")
    assert (rbs.caen.title == "Caen RBS")


def test_make_hardware_config():
    config = {'generic': {'hardware': {
        'aml_1': {'type': 'aml', 'title': 'AML X Y', 'url': 'http://localhost:22000/api/latest',
                  'names': ['X', 'Y'], 'loads': [110, 20]},
        'aml_2': {'type': 'aml', 'title': 'AML Detector Theta', 'url': 'http://localhost:22001/api/latest',
                  'names': ['Detector', 'Theta'], 'loads': [170, 10]},
        'aml_3': {'type': 'aml', 'title': 'AML Phi Zeta', 'url': 'http://localhost:22002/api/latest',
                  'names': ['Phi', 'Zeta'], 'loads': [0, -1]},
        'motrona_4': {'type': 'motrona', 'title': 'Motrona RBS', 'url': 'http://localhost:22100/api/latest'},
        'caen_5': {'type': 'caen', 'title': 'Caen RBS', 'url': 'http://localhost:22200/api/latest'},
        'mdrive_6': {'type': 'mdrive', 'title': 'MDrive', 'url': 'http://localhost:22300/api/latest'}}}}

    hardware = make_hardware_config(config)

    assert (hardware.controllers["aml_1"].title == "AML X Y")
