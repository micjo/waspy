import * as aml from './aml.js'
import * as caen from './caen.js'
import * as con from './daemon_connection.js'

export {onContinueAmlXY, onLoadAmlXY, onSubmitAmlXY, onUnLoadAmlXY};
export {toggleAcquisition, toggleListData, caenClearData, caenSaveHistogram, caenContinueOnError, caenSaveRegistry};
export {onContinueAmlDetTheta, onLoadAmlDetTheta, onSubmitAmlDetTheta, onUnLoadAmlDetTheta};
export {onContinueAmlPhiZeta, onLoadAmlPhiZeta, onSubmitAmlPhiZeta, onUnLoadAmlPhiZeta};
export {caen1};

let caen1 = new caen.caen('http://ubuntu-desktop:22123');
let amlXy = new aml.aml('http://localhost:22000');
let amlDettheta = new aml.aml('http://localhost:22001');
let amlPhizeta = new aml.aml('http://localhost:22002');

async function onMoveAml(prefix, activeAml) {
    let firstMotorRequest = con.getEl(prefix + '_first_request').value;
    let secondMotorRequest = con.getEl(prefix + '_second_request').value;

    if (!firstMotorRequest && !secondMotorRequest) {
        con.collapsableError(prefix+'_request_status', 'Please specify at least 1 motor position');
    }
    await activeAml.moveMotors(firstMotorRequest, secondMotorRequest);
}

function updateAml(prefix, activeAml) {
    con.getEl(prefix + "_first").innerText = activeAml.firstMotorPosition;
    con.getEl(prefix + "_second").innerText = activeAml.secondMotorPosition;
    con.setConnected(prefix + "_connect_status", activeAml.connected);
    con.getEl(prefix + "_request_id").innerText = activeAml.requestId;
    con.getEl(prefix + "_busy_status").innerText = activeAml.busy;
    con.getEl(prefix + "_expiry_date").innerText = activeAml.completionTime;
    con.getEl(prefix + "_time").innerText = con.getUniqueIdentifier();

    if (!activeAml.requestAcknowledge) {
        con.collapsableError(prefix + "_request_status", "Daemon did not acknowledge request");
        activeAml.requestAcknowledge = true;
    }

    con.getEl(prefix+ "_error_status").innerHTML='';
    if (activeAml.error !== "Success") {
        con.collapsableError(prefix + "_error_status", "Daemon error: " +activeAml.error);
    }
}

async function onSubmitAml(prefix, activeAml) {
    con.show(prefix+'_submit_spinner');
    await onMoveAml(prefix, activeAml);
    con.hide(prefix + '_submit_spinner');
    updateAml(prefix, activeAml);
}

async function onLoadAml(prefix, activeAml, firstPos, secondPos) {
    con.getEl(prefix + "_first_request").value = firstPos;
    con.getEl(prefix + "_second_request").value = secondPos;
    con.show(prefix + "_load_spinner", activeAml);
    await onMoveAml(prefix, activeAml);
    con.hide(prefix + "_load_spinner", activeAml);
    updateAml(prefix, activeAml);
}

async function onUnloadAml(prefix, activeAml, firstPos, secondPos) {
    con.getEl(prefix + "_first_request").value = firstPos;
    con.getEl(prefix + "_second_request").value = secondPos;
    con.show(prefix + "_unload_spinner", activeAml);
    await onMoveAml(prefix, activeAml);
    con.hide(prefix + "_unload_spinner", activeAml);
    updateAml(prefix, activeAml);
}

async function onContinueAml(prefix, activeAml) {
    con.show(prefix + "_continue_spinner", activeAml);
    await activeAml.continueOnError();
    con.hide(prefix + "_continue_spinner", activeAml);
    updateAml(prefix, activeAml);
}

function onSubmitAmlXY() {
    onSubmitAml('aml_x_y', amlXy);
}

function onLoadAmlXY() {
    onLoadAml('aml_x_y', amlXy, 50, 30);
}

function onUnLoadAmlXY() {
    onUnloadAml('aml_x_y', amlXy, 40, 20);
}

function onContinueAmlXY() {
    onContinueAml('aml_x_y', amlXy);
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
async function refreshData() {
    await caen1.updateActuals();
    updateCaen();

    await amlXy.updateActuals();
    updateAml('aml_x_y', amlXy);
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
    con.setConnected("caen_connect_status", caen1.connected);
    con.getEl("caen_time").innerText = con.getUniqueIdentifier();

    if (!caen1.requestAcknowledge) {
        con.collapsableError("caen_request_status", "Daemon did not acknowledge request");
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

async function caenSaveHistogram() {
        let folder = con.getEl("caen_histogram_folder_request").value;
        if(folder) {
            con.show("caen_save_histogram_spinner");
            await caen1.saveHistogram(folder);
            con.hide("caen_save_histogram_spinner");
        }
        else {
            con.collapsableError("caen_request_status", "To store the histograms, " +
                "you need to specify a folder");
        }
}

async function caenClearData() {
    con.show("caen_clear_data_spinner");
    await caen1.clearData();
    con.hide("caen_clear_data_spinner");
}

async function caenContinueOnError() {
    con.show("caen_continue_spinner");
    await caen1.continueOnError();
    con.hide("caen_continue_spinner");
}

async function caenSaveRegistry() {
    con.show("caen_save_registry_spinner");
    await caen1.saveRegistry();
    con.hide("caen_save_registry_spinner");
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

