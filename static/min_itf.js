import * as con from './daemon_connection.js'


function setConnected(id, connected) {
    if (connected) {
        console.log("Setting connected !");
        document.getElementById(id).innerText="Connected";
        document.getElementById(id).setAttribute("class","badge badge-success");
    }
    else {
        document.getElementById(id).innerText="Disconnected";
        document.getElementById(id).setAttribute("class","badge badge-danger");
    }
}

function updateConnection(url, id) {
    fetch(url).then(response => {
        console.log(response);
        setConnected(id, response.ok);
    })
    .catch( error => {
        console.log(error);
        setConnected(id,false);
    });
}

function refreshData() {
    updateConnection(con.aml_xy_act, "aml_xy_con");
    updateConnection(con.aml_det_act, "aml_det_theta_con");
    updateConnection(con.aml_phi_act, "aml_phi_zeta_con");
    updateConnection(con.caen_host_1_act, "caen_con");
}

window.setInterval(function() {
    refreshData();
}, 1000);
