lab_urls = {
    "motrona_rbs": "http://127.0.0.1:23000/api/latest",
    "aml_x_y": "http://127.0.0.1:22000/api/latest",
    "aml_det_theta": "http://127.0.0.1:22001/api/latest",
    "aml_phi_zeta": "http://127.0.0.1:22002/api/latest",
    "caen_charles_evans": "http://169.254.13.109:22123/api/latest",
}

home_urls = {
    "motrona_rbs": "http://127.0.0.1:22200/api/latest",
    "aml_x_y": "http://127.0.0.1:22100/api/latest",
    "aml_det_theta": "http://127.0.0.1:22101/api/latest",
    "aml_phi_zeta": "http://127.0.0.1:22102/api/latest",
    "caen_charles_evans": "http://127.0.0.1:22300/api/latest",
}

direct_urls = home_urls

hardware_config = {
        "aml_x_y" : {"type":"aml", "title": "AML X Y", "first_name":"X", "second_name":"Y", "first_load":"72.50", "second_load":"61.7"},
        "aml_phi_zeta" : {"type":"aml", "title": "AML Phi Zeta", "first_name":"Phi", "second_name":"Zeta", "first_load":"0.00", "second_load":"-1.00"},
        "aml_det_theta" : {"type":"aml", "title": "AML Det Theta", "first_name":"Detector", "second_name":"Theta", "first_load":"170.00", "second_load":"-180.50"},
        "motrona_rbs" : {"type":"motrona", "title" : "Motrona RBS"},
        "caen_charles_evans" : {"type":"caen", "title":"CAEN Charles Evans" }
}

watch_dir = "/tmp/watch/"
