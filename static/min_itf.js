import * as con from './daemon_connection.js'

export {onContinueAmlXY, onLoadAmlXY, onSubmitAmlXY, onUnLoadAmlXY};
export {onToggleCaenAcquisition, onToggleCaenListData, onClearData, onSaveHistogram};
export {
    onContinueAmlDetTheta,
    onLoadAmlDetTheta,
    onSubmitAmlDetTheta,
    onUnLoadAmlDetTheta
};
export {
    onContinueAmlPhiZeta,
    onLoadAmlPhiZeta,
    onSubmitAmlPhiZeta,
    onUnLoadAmlPhiZeta
};


function onSubmitMotors(url, id) {
    let firstId = id + '_first_request';
    let secondId = id + '_second_request';
    let first_pos = document.getElementById(firstId).value;
    let second_pos = document.getElementById(secondId).value;
    let requestStatusId = id + '_request_status';

    let request = '';
    if (first_pos && second_pos) {
        request += 'set_m1_target_position=' + first_pos + '\n';
        request += 'set_m2_target_position=' + second_pos + '\n';
        con.sendRequestWithExpiryDate(url, request, id);
    } else if (first_pos) {
        request += 'set_m1_target_position=' + first_pos + '\n';
        con.sendRequestWithExpiryDate(url, request, id);
    } else if (second_pos) {
        request += 'set_m2_target_position=' + second_pos + '\n';
        con.sendRequestWithExpiryDate(url, request, id);
    } else {
        con.collapsableError(requestStatusId, 'No input provided');
    }
}

function onSubmitAmlXY() {
    onSubmitMotors(con.motors.xyUrl, 'aml_x_y');
}
function onLoadAmlXY() {
    con.getEl('aml_x_y_first_request').value = '60';
    con.getEl('aml_x_y_second_request').value = '10';
    onSubmitAmlXY()
}
function onUnLoadAmlXY() {
    con.getEl('aml_x_y_first_request').value = '0';
    con.getEl('aml_x_y_second_request').value = '0';
    onSubmitAmlXY()
}
function onContinueAmlXY() {
    let request = 'continue=true';
    con.sendRequestWithExpiryDate(con.motors.xyUrl, request, 'aml_x_y');
}


function onSubmitAmlDetTheta() {
    onSubmitMotors(con.motors.detThetaUrl, 'aml_det_theta');
}
function onLoadAmlDetTheta() {
    con.getEl('aml_det_theta_first_request').value = '60';
    con.getEl('aml_det_theta_second_request').value = '10';
    onSubmitAmlDetTheta()
}
function onUnLoadAmlDetTheta() {
    con.getEl('aml_det_theta_first_request').value = '0';
    con.getEl('aml_det_theta_second_request').value = '0';
    onSubmitAmlDetTheta()
}
function onContinueAmlDetTheta() {
    let request = 'continue=true';
    con.sendRequestWithExpiryDate(con.motors.detThetaUrl, request, 'aml_det_theta');
}


function onSubmitAmlPhiZeta() {
    onSubmitMotors(con.motors.phiZetaUrl, 'aml_phi_zeta');
}
function onLoadAmlPhiZeta() {
    con.getEl('aml_phi_zeta_first_request').value = '60';
    con.getEl('aml_phi_zeta_second_request').value = '10';
    onSubmitAmlPhiZeta()
}
function onUnLoadAmlPhiZeta() {
    con.getEl('aml_phi_zeta_first_request').value = '0';
    con.getEl('aml_phi_zeta_second_request').value = '0';
    onSubmitAmlPhiZeta()
}
function onContinueAmlPhiZeta() {
    let request = 'continue=true';
    con.sendRequestWithExpiryDate(con.motors.phiZetaUrl, request, 'aml_phi_zeta');
}
function refreshData() {
    //con.getAmlActuals(con.motors.xyUrl, 'aml_x_y');
    //con.getAmlActuals(con.motors.detThetaUrl, 'aml_det_theta');
    //con.getAmlActuals(con.motors.phiZetaUrl, 'aml_phi_zeta');
    // updateConnection(con.dataAcq.caen.responseUrl, "caen_con");
    con.getCaenActuals(con.dataAcq.caenUrl, 'caen');
}

// this should also be updated from the actuals - in html default show '-' , then update based on actuals
function onToggleCaenAcquisition() {
    con.toggleCaenAcquisitionState('caen');
}

function onToggleCaenListData() {
    con.toggleCaenListDataState('caen');
}

function onClearData() {

}

function onSaveHistogram() {

}

window.setInterval(function() {
    refreshData();
}, 2000);

