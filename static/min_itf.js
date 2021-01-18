import * as aml from './aml.js'
import * as caen from './caen.js'
import * as con from './daemon_connection.js'

export {onContinueAmlXY, onLoadAmlXY, onSubmitAmlXY, onUnLoadAmlXY};
export {toggleAcquisition, toggleListData, saveHistogram};
export {onContinueAmlDetTheta, onLoadAmlDetTheta, onSubmitAmlDetTheta, onUnLoadAmlDetTheta};
export {onContinueAmlPhiZeta, onLoadAmlPhiZeta, onSubmitAmlPhiZeta, onUnLoadAmlPhiZeta};
export {caen1};

let caen1 = new caen.caen('http://ubuntu-desktop:22123');
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
    updateCaen();
    // amlXy.updateActuals();
    // amlDettheta.updateActuals();
    // amlPhizeta.updateActuals();
}


function updateCaen() {
    updateAcquireButton();
    updateListDataButton();
    con.getEl("caen_request_id").innerText = caen1.requestId;
    con.getEl("caen_acquiring_data").innerText = caen1.acquiringData;
    con.getEl("caen_storing_list_data").innerText = caen1.listDataSaving;
    con.getEl("caen_histogram_folder").innerText = caen1.histogramLocation;
    con.getEl("caen_list_data_folder").innerText = caen1.listDataLocation;
    con.getEl("caen_list_data_timeout").innerText = caen1.listDataTimeout;

    if (!caen1.requestAcknowledge) {
        con.collapsableError("caen_request_status", "Daemon did not acknowledge response");
        caen1.requestAcknowledge = true;
    }

    if (caen1.error !== "Success") {
        con.getEl("caen_error_status").innerHTML='';
        con.collapsableError("caen_error_status", "Daemon error: " + caen1.error);
        caen1.error = "Success";
    }
}

async function toggleAcquisition() {
    con.show("caen_toggle_acquisition_spinner");
    await caen1.toggleAcquire();
    con.hide("caen_toggle_acquisition_spinner");
    updateCaen();
}

async function toggleListData() {
    let listDataTry = caen1.listDataSaving;
    listDataTry = !listDataTry;
    if (listDataTry){
        let folder = con.getEl("caen_list_data_folder_request").value;
        let timeout = con.getEl("caen_list_data_timeout_request").value;
        if (folder && timeout) {
            con.show("caen_toggle_list_data_spinner");
            await caen1.startStoringListData(folder, timeout);
            con.hide("caen_toggle_list_data_spinner");
        }
        else {
            con.collapsableError("caen_request_status", "To store list data, " +
                "you need to specify folder and timeout.");
        }

    }
    else {
        con.show("caen_toggle_list_data_spinner");
        await caen1.stopStoringListData();
        con.hide("caen_toggle_list_data_spinner");
    }
    updateCaen();
}

function saveHistogram() {
        let folder = con.getEl("caen_histogram_folder_request").value;
        if(folder) {
            caen1.saveHistogram(folder);
        }
        else {
            con.collapsableError("caen_request_status", "To store the histograms, " +
                "you need to specify a folder");
        }
}

function updateListDataButton() {
    if (caen1.listDataSaving) {
        con.setButtonOn("caen_toggle_list_data");
        con.getEl("caen_toggle_list_data_text").innerText = "Saving list data";
    }
    else {
        con.setButtonOff("caen_toggle_list_data");
        con.getEl("caen_toggle_list_data_text").innerText = "Not saving list data";

    }
}

function updateAcquireButton() {
    if (caen1.acquiringData) {
        con.setButtonOn("caen_toggle_acquisition");
        con.getEl("caen_toggle_acquisition_text").innerText = "Acquiring data";
    }
    else {
        con.setButtonOff("caen_toggle_acquisition");
        con.getEl("caen_toggle_acquisition_text").innerText = "Not acquiring data";
    }
}

window.setInterval(function() {
    refreshData();
}, 2000);

