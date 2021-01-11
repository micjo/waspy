import * as con from './daemon_connection.js'

export {onSubmitAmlXY, onLoadAmlXY, onUnLoadAmlXY, onContinueAmlXY}
export {onSubmitAmlDetTheta, onLoadAmlDetTheta, onUnLoadAmlDetTheta}
export {onSubmitAmlPhiZeta, onLoadAmlPhiZeta, onUnLoadAmlPhiZeta}

function updateConnection(url, id) {
    fetch(url).then(response => {
        setConnected(id, response.ok);
    })
    .catch( error => {
        setConnected(id,false);
    });
}

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

function onSubmitAmlXY() {
    onSubmitMotors(con.motors.xyUrl, 'aml_x_y_request_status', 'aml_x_request', 'aml_y_request');
}

function onLoadAmlXY() {
    con.getEl('aml_x_request').value = '60';
    con.getEl('aml_y_request').value = '10';
    onSubmitAmlXY()
}

function onUnLoadAmlXY() {
    con.getEl('aml_x_request').value = '0';
    con.getEl('aml_y_request').value = '0';
    onSubmitAmlXY()
}

function onContinueAmlXY() {
    let url = con.motors.xyUrl;

    let requestId = con.getUniqueIdentifier();
    let request = "request_id="+requestId+"\n";
    request += "continue=true";
    let statusId = "aml_x_y_status";
    con.sendRequest(url, requestId, request, "aml_x_y_request_status");
}

function onSubmitAmlDetTheta() {
    //onSubmitMotors(con.motors.xy.requestUrl, 'aml_det_theta_status', 'aml_det_request', 'aml_theta_request');
}

function onLoadAmlDetTheta() {
    con.getEl('aml_det_request').value = '60';
    con.getEl('aml_theta_request').value = '10';
    onSubmitAmlDetTheta();
}

function onUnLoadAmlDetTheta() {
    con.getEl('aml_det_request').value = '0';
    con.getEl('aml_theta_request').value = '0';
    onSubmitAmlDetTheta();
}

function onSubmitAmlPhiZeta() {
    //onSubmitMotors(con.motors.xy.requestUrl, 'aml_phi_zeta_status', 'aml_phi_request', 'aml_zeta_request');
}

function onLoadAmlPhiZeta() {
    con.getEl('aml_phi_request').value = '60';
    con.getEl('aml_zeta_request').value = '10';
    onSubmitAmlPhiZeta();
}

function onUnLoadAmlPhiZeta() {
    con.getEl('aml_phi_request').value = '0';
    con.getEl('aml_zeta_request').value = '0';
    onSubmitAmlPhiZeta();
}

function onSubmitMotors(url, statusId, firstId, secondId) {
    console.log("onsubmit motors");
    let first_pos = document.getElementById(firstId).value;
    let second_pos = document.getElementById(secondId).value;
    let requestId = con.getUniqueIdentifier();

    let request = "request_id="+requestId+"\n";
    if (first_pos && second_pos) {
        request += "set_m1_target_position=" + first_pos + "\n";
        request += "set_m2_target_position=" + second_pos + "\n";
        con.sendRequest(url, requestId, request, statusId);
    }
    else if (first_pos) {
        request += "set_m1_target_position=" + first_pos + "\n";
        con.sendRequest(url, requestId, request, statusId);
    }
    else if (second_pos) {
        request += "set_m2_target_position=" + second_pos + "\n";
        con.sendRequest(url, requestId, request, statusId);
    }
    else {
        con.collapsableError(statusId, "No input provided");
    }
}

function updateMotors(url, connectionId, errorId, busyId, firstMotorId, secondMotorId) {
    fetch(url + "/actuals")
    .then(response => {
        setConnected(connectionId, response.ok);
        return response.json();
    })
    .then( data => {
        con.getEl(firstMotorId).innerText = data["motor1"]["position_real_world"];
        con.getEl(secondMotorId).innerText = data["motor2"]["position_real_world"];
        if (data["error_status"] !== "Success") {
            con.collapsableError(errorId, data["error_status"]);
        }
        else {
            con.getEl(errorId).innerHTML="";
        }

        if (data["status"] === "Processing") {
            con.getEl(busyId).style.display="block";
        }
        else if (data["status"] === "Done") {
            con.getEl(busyId).style.display="none";
        }
    })
    .catch( error => {
        setConnected(connectionId, false);
        con.collapsableError(errorId, error);
    });
}

function refreshData() {
    updateMotors(con.motors.xyUrl, "amlXyConnected", "aml_x_y_error_status", "aml_x_y_busy_status", "aml_x", "aml_y");
    //updateMotors(con.motors.detTheta.responseUrl, "amlDetThetaConnected", "aml_det", "aml_theta");
    //updateMotors(con.motors.phiZeta.responseUrl, "amlPhiZetaConnected", "aml_phi", "aml_zeta");
    //updateConnection(con.dataAcq.caen.responseUrl, "caen_con");
}

window.setInterval(function() {
    refreshData();
}, 2000);
