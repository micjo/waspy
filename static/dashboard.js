import * as aml from './controllers/aml.js'
import * as con from './controllers/daemon_connection.js'

let amlXy = new aml.aml('http://169.254.166.218:22000');
let amlDetTheta = new aml.aml('http://169.254.166.218:22001');
let amlPhiZeta = new aml.aml('http://169.254.166.218:22002');

function updateDaemon(prefix, activeDaemon) {
    con.setConnected(prefix + "_connect_status", activeDaemon.connected);
    con.setBadgeState(prefix + "_error_status", activeDaemon.error !== "Success");
    con.getEl(prefix + "_error_status").innerText = activeDaemon.error;
    con.getEl(prefix + "_request_id").innerText = activeDaemon.requestId;
}

async function refreshData() {
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
