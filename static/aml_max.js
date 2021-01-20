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

export { toggleFirstMotorPos, toggleFirstMotorTemperature, getMotorOnePos, getMotorOneTemp};
export { redefineFirstStep, redefineFirstPos, redefineFirstOffset };
export { submit, load, continueOnError };


let currentAml;
let prefix;

function makeAml(pref, url) {
    console.log(pref);
    console.log(url);
    currentAml = new aml.aml(url);
    prefix = pref;
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


async function toggleFirstMotorPos() {
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

function toggleFirstMotorTemperature() {
}
async function getMotorOnePos() {
    con.show(prefix+'_get_motor_one_pos_spinner');
    await currentAml.getFirstPosition();
    con.hide(prefix + '_get_motor_one_pos_spinner');
    updateAmlExtended();
}

async function getMotorOneTemp() {
    con.show(prefix+'_get_motor_one_temperature_spinner');
    await currentAml.getFirstTemperature();
    con.hide(prefix + '_get_motor_one_temperature_spinner');
    updateAmlExtended();
}

function continueOnError() {
     itf.onContinueAml(prefix, currentAml);
}

function submit() {
    itf.onSubmitAml(prefix, currentAml);
}

function load() {
    itf.onLoadAml(prefix, currentAml, 10, 10);
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
