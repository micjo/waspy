import * as con from './daemon_connection.js'

export {onSubmitAmlXy}

function setConnected(id, connected) {
    if (connected) {
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
        setConnected(id, response.ok);
    })
    .catch( error => {
        console.log(error);
        setConnected(id,false);
    });
}

function onSubmitAmlXy() {
    console.log("submit aml xy");
    let x_pos = document.getElementById("aml_x").value;
    let y_pos = document.getElementById("aml_y").value;
    console.log(x_pos);
    console.log(y_pos);

    let request = con.getUniqueIdentifier();
    if (x_pos && y_pos) {
        request += "set_m1_target_position=" + x_pos + "\n";
        request += "set_m2_target_position=" + y_pos + "\n";
        con.sendRequest(con.aml_xy_request, request);
    }
    else if (x_pos) {
        request += "set_m1_target_position=" + x_pos + "\n";
        con.sendRequest(con.aml_xy_request, request);
    }
    else if (y_pos) {
        request += "set_m2_target_position=" + y_pos + "\n";
        con.sendRequest(con.aml_xy_request, request);
    }
    else {
        con.collapsableError("#collapseExample", "No input provided");
    }
}

function updateActualsAmlXy() {
    console.log("update actuals XY");
    fetch(con.aml_xy_response)
        .then(response => response.json())
        .then(data => {
            con.getEl("aml_x").innerText = data["motor1"]["position_real_world"];
            con.getEl("aml_y").innerText = data["motor2"]["position_real_world"];
        });
}

function refreshData() {
    updateConnection(con.aml_xy_response, "aml_xy_con");
    updateActualsAmlXy();
    updateConnection(con.aml_det_response, "aml_det_theta_con");
    updateConnection(con.aml_phi_response, "aml_phi_zeta_con");
    updateConnection(con.caen_host_1_response, "caen_con");
}

//document.getElementById('aml_xy_submit').addEventListener('onclick', onSubmitAmlXy)

window.setInterval(function() {
    refreshData();
}, 2000);
