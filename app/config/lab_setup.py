from app.config.entities import DaemonConfig, OutputDirConfig, InputDirConfig

daemons = DaemonConfig.parse_raw('''{
    "aml_x_y" : {"type":"aml", "title": "AML X Y", "first_name":"X", "second_name":"Y", "first_load":72.50, "second_load":61.7, "url": "http://127.0.0.1:22000/api/latest"},
    "aml_det_theta" : {"type":"aml", "title": "AML Det Theta", "first_name":"Detector", "second_name":"Theta", "first_load":170.00, "second_load":-180.50, "url":"http://127.0.0.1:22001/api/latest"},
    "aml_phi_zeta" : {"type":"aml", "title": "AML Phi Zeta", "first_name":"Phi", "second_name":"Zeta", "first_load":0.00, "second_load":-1.00, "url":"http://127.0.0.1:22002/api/latest"},
    "motrona_rbs" : {"type":"motrona", "title" : "Motrona RBS", "url":"http://127.0.0.1:23000/api/latest"},
    "caen_charles_evans" : {"type":"caen", "title":"CAEN Charles Evans", "url":"http://169.254.13.109:22123/api/latest" }
    }''')

input_dir = InputDirConfig.parse_raw('''{
    "watch": "C:/ACQ/_01_watch"
}''')

output_dir = OutputDirConfig.parse_raw('''{
    "ongoing": "C:/ACQ/_02_ongoing",
    "done": "C:/ACQ/_03_done",
    "failed": "C:/ACQ/_04_failed",
    "data": "C:/ACQ/_05_data"
}''')

output_dir_remote = OutputDirConfig.parse_raw('''{
    "ongoing": "W:/transfer_RBS/ACQ/2_ongoing",
    "done": "W:/transfer_RBS/ACQ/3_done",
    "failed": "W:/transfer_RBS/ACQ/4_failed",
    "data": "W:transfer_RBS/ACQ/5_data"
}''')


