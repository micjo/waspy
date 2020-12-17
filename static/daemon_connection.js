export {aml_xy_act, aml_det_act, aml_phi_act, caen_host_1_act}

let aml_host = 'http://localhost'
let caen_host = 'http://localhost'

let aml_xy = aml_host + ":22000"
let aml_det = aml_host + ":22001"
let aml_phi = aml_host + ":22002"
let caen_host_1 = caen_host + "22003"

let aml_xy_act = aml_xy + "/actuals"
let aml_det_act = aml_det + "/actuals"
let aml_phi_act = aml_phi + "/actuals"
let caen_host_1_act = caen_host_1 + "22003" + "/actuals"
