import * as con from './daemon_connection.js'

export {onSubmitAmlXY}

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
    console.log("submit aml xy");
    let x_pos = document.getElementById("aml_x_request").value;
    let y_pos = document.getElementById("aml_y_request").value;
    console.log(x_pos);
    console.log(y_pos);

    let request = con.getUniqueIdentifier();
    if (x_pos && y_pos) {
        request += "set_m1_target_position=" + x_pos + "\n";
        request += "set_m2_target_position=" + y_pos + "\n";
        con.sendRequest(con.motors.xy.requestUrl, request);
    }
    else if (x_pos) {
        request += "set_m1_target_position=" + x_pos + "\n";
        con.sendRequest(con.motors.xy.requestUrl, request);
    }
    else if (y_pos) {
        request += "set_m2_target_position=" + y_pos + "\n";
        con.sendRequest(con.motors.xy.requestUrl, request);
    }
    else {
        con.collapsableError("#collapseExample", "No input provided");
    }
}

function updateMotors(url, connectionId, firstMotorId, secondMotorId) {
    fetch(url)
        .then(response => {
            setConnected(connectionId, response.ok);
            return response.json();
        })
        .then( data => {
            con.getEl(firstMotorId).innerText = data["motor1"]["position_real_world"];
            con.getEl(secondMotorId).innerText = data["motor2"]["position_real_world"];
        })
        .catch( error => {
            setConnected(connectionId, false);
        });
}


function refreshData() {
    updateMotors(con.motors.xy.responseUrl, "amlXyConnected", "aml_x", "aml_y");
    updateMotors(con.motors.detTheta.responseUrl, "amlDetThetaConnected", "aml_det", "aml_theta");
    updateMotors(con.motors.phiZeta.responseUrl, "amlPhiZetaConnected", "aml_phi", "aml_zeta");
    updateConnection(con.dataAcq.caen.responseUrl, "caen_con");
}

window.setInterval(function() {
    refreshData();
}, 2000);
