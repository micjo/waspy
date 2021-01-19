import * as aml from './aml.js'
import * as caen from './caen.js'
import * as con from './daemon_connection.js'

let caen1 = new caen.caen('http://ubuntu-desktop:22123', 'caen');

let amlXy = new aml.aml('http://localhost:22000');
let amlDetTheta = new aml.aml('http://localhost:22001');
let amlPhiZeta = new aml.aml('http://localhost:22002');

function updateCaen() {
    con.setConnected("caen_connect_status", caen1.connected);
    con.setBadgeState("caen_error_status", caen1.error !== "Success");
    con.getEl("caen_error_status").innerText = caen1.error;
    con.getEl("caen_request_id").innerText = caen1.requestId;

    if (caen1.acquiringData) {
        con.getEl("caen_acquiring_data").innerText = "Acquiring active";
    }
    else {
        con.getEl("caen_acquiring_data").innerText = "-";
    }
}

function updateDaemon(prefix, activeDaemon) {
    con.setConnected(prefix + "_connect_status", activeDaemon.connected);
    con.setBadgeState(prefix + "_error_status", activeDaemon.error !== "Success");
    con.getEl(prefix + "_error_status").innerText = activeDaemon.error;
    con.getEl(prefix + "_request_id").innerText = activeDaemon.requestId;
}

async function refreshData() {
    await caen1.updateActuals();
    updateCaen();
    await amlXy.updateActuals();
    updateDaemon('aml_x_y', amlXy);
    await amlDetTheta.updateActuals();
    updateDaemon('aml_det_theta', amlDetTheta);
    await amlPhiZeta.updateActuals();
    updateDaemon('aml_phi_zeta', amlPhiZeta);
}

window.setInterval(function() {
    refreshData();
}, 2000);
