from app.setup.entities import DaemonConfig, OutputDirConfig, InputDirConfig

daemons = DaemonConfig.parse_raw('''{
    "aml_x_y" : {"type":"aml", "title": "AML X Y", "first_name":"X", "second_name":"Y", "first_load":74, "second_load":61.0, "url": "http://127.0.0.1:22000/api/latest"},
    "aml_det_theta" : {"type":"aml", "title": "AML Det Theta", "first_name":"Detector", "second_name":"Theta", "first_load":170.00, "second_load":-180.50, "url":"http://127.0.0.1:22001/api/latest"},
    "aml_phi_zeta" : {"type":"aml", "title": "AML Phi Zeta", "first_name":"Phi", "second_name":"Zeta", "first_load":0.00, "second_load":-2.2, "url":"http://127.0.0.1:22002/api/latest"},
    "motrona_rbs" : {"type":"motrona", "title" : "Motrona RBS", "url":"http://127.0.0.1:23000/api/latest"},
    "caen_rbs" : {"type":"caen", "title":"CAEN RBS", "url":"http://169.254.80.218:22300/api/latest" }
    }''')

input_dir = InputDirConfig.parse_raw('''{
    "watch": "/mnt/mcaiba_nas/1_watch"
}''')

output_dir = OutputDirConfig.parse_raw('''{
    "ongoing": "/mnt/mcaiba_nas/2_ongoing",
    "done": "/mnt/mcaiba_nas/3_done",
    "failed": "/mnt/mcaiba_nas/4_failed",
    "data": "/mnt/mcaiba_nas/5_data"
}''')

output_dir_remote = OutputDirConfig.parse_raw('''{
    "ongoing": "/mnt/winbe_wasp/_02_ongoing",
    "done": "/mnt/winbe_wasp/_03_done",
    "failed": "/mnt/winbe_wasp/_04_failed",
    "data": "/mnt/winbe_wasp/_05_data"
}''')
