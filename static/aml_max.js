import * as aml from './aml.js'
import * as itf from './itf.js'
import * as con from './daemon_connection.js'

// TODO: move itf functionality in here gradually:
// add function : makeAml('prefix','url') and add this to a dictionary
// then all onclick calls in html will have to specify what the prefix is to select the wanted aml
// This allows for reusability and will prepare for a more dynamic setup
//
// the jinja values get passed from the server running python
// into html so they have to make it into the javascript somehow
// This is a construct that can work

export {makeAml, refreshData};

export { toggleFirstPos, toggleFirstTemperature, getFirstPos, getFirstTemp};
export { redefineFirstStep, redefineFirstPos, redefineFirstOffset };


export { toggleSecondPos, toggleSecondTemperature, getSecondPos, getSecondTemp};
export { redefineSecondStep, redefineSecondPos, redefineSecondOffset };
export { submit, load, continueOnError, hide, show };

let currentAml;
let prefix;
let firstLoadPos;
let secondLoadPos;

function makeAml(pref, url, loadFirst, loadSecond) {
    currentAml = new aml.aml(url);
    prefix = pref;
    firstLoadPos = loadFirst;
    secondLoadPos = loadSecond;
}

function updateAmlExtended() {
    itf.updateAml(prefix, currentAml);
    con.getEl(prefix + "_first_temperature").innerText = currentAml.firstMotorTemperature;
    con.getEl(prefix + "_first_step").innerText = currentAml.firstMotorStepCounter;
    con.getEl(prefix + "_first_position").innerText = currentAml.firstMotorPosition;
    con.getEl(prefix + "_first_offset").innerText = currentAml.firstMotorOffset;

    con.getEl(prefix + "_second_temperature").innerText = currentAml.secondMotorTemperature;
    con.getEl(prefix + "_second_step").innerText = currentAml.secondMotorStepCounter;
    con.getEl(prefix + "_second_position").innerText = currentAml.secondMotorPosition;
    con.getEl(prefix + "_second_offset").innerText = currentAml.secondMotorOffset;
}

async function refreshData() {
    await currentAml.updateActuals();
    updateAmlExtended();
}


function continueOnError() {
     itf.onContinueAml(prefix, currentAml);
}

function submit() {
    itf.onSubmitAml(prefix, currentAml);
}

function load() {
    itf.onLoadAml(prefix, currentAml, firstLoadPos, secondLoadPos);
}

function hide() {
    itf.onHideAml(prefix, currentAml);
}

function show() {
    itf.onShowAml(prefix, currentAml);
}

async function toggleFirstPos() {
    con.show(prefix+'_toggle_first_position_spinner');
    await currentAml.toggleFirstPositionUpdate();
    con.hide(prefix+'_toggle_first_position_spinner');

    if (currentAml.gettingFirstPos) {
        con.setButtonOn(prefix+ "_toggle_first_position_button");
        con.getEl(prefix + "_toggle_first_position_text").innerText = "Updating position";
    }
    else {
        con.setButtonOff(prefix+ "_toggle_first_position_button");
        con.getEl(prefix + "_toggle_first_position_text").innerText = "Not updating position";
    }
}

async function toggleFirstTemperature() {
    con.show(prefix+'_toggle_first_temperature_spinner');
    await currentAml.toggleFirstTemperatureUpdate();
    con.hide(prefix+'_toggle_first_temperature_spinner');

    if (currentAml.gettingFirstTemp) {
        con.setButtonOn(prefix+ "_toggle_first_temperature_button");
        con.getEl(prefix + "_toggle_first_temperature_text").innerText = "Updating temperature";
    }
    else {
        con.setButtonOff(prefix+ "_toggle_first_temperature_button");
        con.getEl(prefix + "_toggle_first_temperature_text").innerText = "Not updating temperature";
    }

}
async function getFirstPos() {
    con.show(prefix+'_get_first_pos_spinner');
    await currentAml.getFirstPosition();
    con.hide(prefix + '_get_first_pos_spinner');
    updateAmlExtended();
}

async function getFirstTemp() {
    con.show(prefix+'_get_first_temperature_spinner');
    await currentAml.getFirstTemperature();
    con.hide(prefix + '_get_first_temperature_spinner');
    updateAmlExtended();
}

async function redefineFirstStep() {
    let newValue = con.getEl(prefix+'_first_step_request').value;
    if (!newValue) {
        con.collapsableError(prefix + "_request_status",
            "Please specify a new value for the motor step counter");
        return;
    }
    con.show(prefix+"_first_step_spinner");
    await currentAml.redefineFirstStepCounter(newValue);
    con.hide(prefix+"_first_step_spinner");
    updateAmlExtended();
}

async function redefineFirstPos() {
    let newValue = con.getEl(prefix+'_first_position_request').value;
    if (!newValue) {
        con.collapsableError(prefix + "_request_status",
            "Please specify a new value for the motor position");
        return;
    }
    con.show(prefix + "_first_position_spinner");
    await currentAml.redefineFirstPosition(newValue);
    con.hide(prefix + "_first_position_spinner");
    updateAmlExtended();
}

async function redefineFirstOffset() {
    let newValue = con.getEl(prefix+'_first_offset_request').value;
    if (!newValue) {
        con.collapsableError(prefix + "_request_status",
            "Please specify a new value for the motor position");
        return;
    }
    con.show(prefix + "_first_offset_spinner");
    await currentAml.redefineFirstOffset(newValue);
    con.hide(prefix + "_first_offset_spinner");
    updateAmlExtended();
}



async function toggleSecondPos() {
    con.show(prefix+'_toggle_second_position_spinner');
    await currentAml.toggleSecondPositionUpdate();
    con.hide(prefix+'_toggle_second_position_spinner');

    if (currentAml.gettingSecondPos) {
        con.setButtonOn(prefix+ "_toggle_second_position_button");
        con.getEl(prefix + "_toggle_second_position_text").innerText = "Updating position";
    }
    else {
        con.setButtonOff(prefix+ "_toggle_second_position_button");
        con.getEl(prefix + "_toggle_second_position_text").innerText = "Not updating position";
    }
}

async function toggleSecondTemperature() {
    con.show(prefix+'_toggle_second_temperature_spinner');
    await currentAml.toggleSecondTemperatureUpdate();
    con.hide(prefix+'_toggle_second_temperature_spinner');

    if (currentAml.gettingSecondTemp) {
        con.setButtonOn(prefix+ "_toggle_second_temperature_button");
        con.getEl(prefix + "_toggle_second_temperature_text").innerText = "Updating temperature";
    }
    else {
        con.setButtonOff(prefix+ "_toggle_second_temperature_button");
        con.getEl(prefix + "_toggle_second_temperature_text").innerText = "Not updating temperature";
    }

}
async function getSecondPos() {
    con.show(prefix+'_get_second_pos_spinner');
    await currentAml.getSecondPosition();
    con.hide(prefix + '_get_second_pos_spinner');
    updateAmlExtended();
}

async function getSecondTemp() {
    con.show(prefix+'_get_second_temperature_spinner');
    await currentAml.getSecondTemperature();
    con.hide(prefix + '_get_second_temperature_spinner');
    updateAmlExtended();
}

async function redefineSecondStep() {
    let newValue = con.getEl(prefix+'_second_step_request').value;
    if (!newValue) {
        con.collapsableError(prefix + "_request_status",
            "Please specify a new value for the motor step counter");
        return;
    }
    con.show(prefix+"_second_step_spinner");
    await currentAml.redefineSecondStepCounter(newValue);
    con.hide(prefix+"_second_step_spinner");
    updateAmlExtended();
}

async function redefineSecondPos() {
    let newValue = con.getEl(prefix+'_second_position_request').value;
    if (!newValue) {
        con.collapsableError(prefix + "_request_status",
            "Please specify a new value for the motor position");
        return;
    }
    con.show(prefix + "_second_position_spinner");
    await currentAml.redefineSecondPosition(newValue);
    con.hide(prefix + "_second_position_spinner");
    updateAmlExtended();
}
async function redefineSecondOffset() {
    let newValue = con.getEl(prefix+'_second_offset_request').value;
    if (!newValue) {
        con.collapsableError(prefix + "_request_status",
            "Please specify a new value for the motor position");
        return;
    }
    con.show(prefix + "_second_offset_spinner");
    await currentAml.redefineSecondOffset(newValue);
    con.hide(prefix + "_second_offset_spinner");
    updateAmlExtended();
}
