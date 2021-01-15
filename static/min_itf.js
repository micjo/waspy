import * as aml from './aml.js'
import * as caen from './caen.js'
import * as con from './daemon_connection.js'

export {onContinueAmlXY, onLoadAmlXY, onSubmitAmlXY, onUnLoadAmlXY};
export {
    onContinueCaen,
    onSaveHistogram,
    onToggleCaenAcquisition,
    onToggleCaenListData
};
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

export {caen1}

let caen1 = new caen.caen('http://ubuntu-desktop:22123', 'caen');
let amlXy = new aml.aml('http://localhost:22000', 'aml_x_y');
let amlDettheta = new aml.aml('http://localhost:22001', 'aml_det_theta');
let amlPhizeta = new aml.aml('http://localhost:22002', 'aml_phi_zeta');

function onSubmitAmlXY() {
    amlXy.submitMotors();
}

function onLoadAmlXY() {
    amlXy.loadMotors();
}

function onUnLoadAmlXY() {
    amlXy.unLoadMotors();
}

function onContinueAmlXY() {
    amlXy.continueOnError();
}

function onSubmitAmlDetTheta() {
    amlDettheta.submitMotors();
}
function onLoadAmlDetTheta() {
    amlDettheta.loadMotors();
}
function onUnLoadAmlDetTheta() {
    amlDettheta.unLoadMotors();
}
function onContinueAmlDetTheta() {
    amlDettheta.continueOnError();
}

function onSubmitAmlPhiZeta() {
    amlPhizeta.submitMotors();
}
function onLoadAmlPhiZeta() {
    amlPhiZeta.loadMotors();
}
function onUnLoadAmlPhiZeta() {
    amlPhiZeta.unloadMotors();
}
function onContinueAmlPhiZeta() {
    amlPhiZeta.continueOnError();
}
function refreshData() {
    caen1.updateActuals();
    // amlXy.updateActuals();
    // amlDettheta.updateActuals();
    // amlPhizeta.updateActuals();
}

// this should also be updated from the actuals - in html default show '-' ,
// then update based on actuals
//
//
function onToggleCaenAcquisition() {
    caen1.toggleAcquisition();
}

function onToggleCaenListData() {
    caen1.toggleListData();
}

function onContinueCaen() {
    caen1.continueOnError();
}

function onSaveHistogram() {}

window.setInterval(function() {
    refreshData();
}, 2000);

