from app.setup.entities import DaemonConfig, OutputDirConfig, InputDirConfig

daemons = DaemonConfig.parse_raw('''{
    "aml_x_y" : {"type":"aml", "title": "AML X Y", "first_name":"X", "second_name":"Y", "first_load":72.50, "second_load":61.7, "url": "http://127.0.0.1:22100/api/latest"},
    "aml_det_theta" : {"type":"aml", "title": "AML Det Theta", "first_name":"Detector", "second_name":"Theta", "first_load":170.00, "second_load":-180.50, "url":"http://127.0.0.1:22100/api/latest"},
    "aml_phi_zeta" : {"type":"aml", "title": "AML Phi Zeta", "first_name":"Phi", "second_name":"Zeta", "first_load":0.00, "second_load":-1.00, "url":"http://127.0.0.1:22100/api/latest"},
    "motrona_rbs" : {"type":"motrona", "title" : "Motrona RBS", "url":"http://127.0.0.1:22300/api/latest"},
    "caen_rbs" : {"type":"caen", "title":"CAEN RBS", "url":"http://127.0.0.1:22200/api/latest" }
    }''')

input_dir = InputDirConfig.parse_raw('''{
    "watch": "/tmp/ACQ/1_watch"
}''')

output_dir = OutputDirConfig.parse_raw('''{
    "ongoing": "/tmp/ACQ/2_ongoing",
    "done": "/tmp/ACQ/3_done",
    "failed": "/tmp/ACQ/4_failed",
    "data": "/tmp/ACQ/5_data"
}''')

output_dir_remote = OutputDirConfig.parse_raw('''{
    "ongoing": "/tmp/REM/ACQ/2_ongoing",
    "done": "/tmp/REM/ACQ/3_done",
    "failed": "/tmp/REM/ACQ/4_failed",
    "data": "/tmp/REM/ACQ/5_data"
}''')