import * as con from './daemon_connection.js'

export {
    load,
    submit,
    updateUi,
    setMaxMode,
    sendARequest,
    sendInt,
    sendString,
    sendFloat,
    toggle,
    refreshData
}

let maxMode = false;
function setMaxMode() {
    maxMode = true;
}

async function refreshData(url,prefix) {
    let hwData = await con.getStatus(url)
    updateUi(prefix, hwData);
}


function updateUi(prefix, hwData) {
    if (!hwData) {
        con.setBadgeStateWithText(prefix + "_connect_status" , false, "Not Active");
        return;
    }
    con.setBadgeStateWithText(prefix + "_connect_status" , true, "Active");

    con.updateElement(prefix + '_request_id', hwData["request_id"]);
    con.updateElement(prefix + '_request_finished', hwData["request_finished"]);
    con.updateElement(prefix + '_expiry', hwData["expiry_date"]);
    con.updateElement(prefix + '_error', hwData["error"]);
    con.updateElement(prefix + '_first', hwData["motor_1_position"]);
    con.updateElement(prefix + '_second', hwData["motor_2_position"]);

    if (maxMode) {
        con.updateElement(prefix + '_first_position', hwData["motor_1_position"]);
        con.updateElement(prefix + '_adv_first_position', hwData["motor_1_position"]);
        con.updateElement(prefix + '_first_temperature', hwData["motor_1_temperature"]);
        con.updateElement(prefix + '_first_step', hwData["motor_1_steps"]);
        con.updateElement(prefix + '_first_offset', hwData["motor_1_offset"]);
        con.updateElement(prefix + '_update_m1_position', hwData["motor_1_updating_position"]);
        con.updateElement(prefix + '_update_m1_temperature', hwData["motor_1_updating_temperature"]);

        con.updateElement(prefix + '_second_position', hwData["motor_2_position"]);
        con.updateElement(prefix + '_adv_second_position', hwData["motor_2_position"]);
        con.updateElement(prefix + '_second_temperature', hwData["motor_2_temperature"]);
        con.updateElement(prefix + '_second_step', hwData["motor_2_steps"]);
        con.updateElement(prefix + '_second_offset', hwData["motor_2_offset"]);
        con.updateElement(prefix + '_update_m2_position', hwData["motor_2_updating_position"]);
        con.updateElement(prefix + '_update_m2_temperature', hwData["motor_2_updating_temperature"]);

        con.updateElement(prefix + '_debug_rs232', hwData["debug_rs232"]);
        con.updateElement(prefix + '_debug_aml', hwData["debug_aml"]);
        con.updateElement(prefix + '_debug_broker', hwData["debug_broker"]);

        con.getEl(prefix + "_update_m1_position_click").checked = hwData["motor_1_updating_position"];
        con.getEl(prefix + "_update_m1_temperature_click").checked = hwData["motor_1_updating_temperature"];
        con.getEl(prefix + "_debug_rs232_click").checked = hwData["debug_rs232"];
        con.getEl(prefix + "_debug_aml_click").checked = hwData["debug_aml"];
        con.getEl(prefix + "_debug_broker_click").checked = hwData["debug_broker"];
    }

}

function submit(url, prefix, id) {
    let pos1 = parseFloat(con.getEl(prefix + "_first_request").value);
    let pos2 = parseFloat(con.getEl(prefix + "_second_request").value);

    if (isNaN(pos1)|| isNaN(pos2)) {
        con.showFailureModal('Invalid input. Numbers are expected for motor positions.');
        return;
    }

    let request = {};
    request["set_m1_target_position"] = pos1;
    request["set_m2_target_position"] = pos2;
    con.sendRequestAndSpin(url, prefix, id, request);
}

function load(prefix, firstPos, secondPos){
    con.getEl(prefix + "_first_request").value = firstPos;
    con.getEl(prefix + "_second_request").value = secondPos;
}

async function sendARequest(url, prefix, id ,request) {
    let data = await con.sendARequest(url, prefix, id, request);
    updateUi(prefix, data);
}

async function sendInt(url,prefix, id, requestKey) {
    let data = await con.sendInt(url,prefix, id, requestKey);
    updateUi(prefix, data);
}

async function sendString(url,prefix, id, requestKey) {
    let data = await con.sendString(url,prefix, id, requestKey);
    updateUi(prefix, data);
}

async function sendFloat(url,prefix, id, requestKey) {
    let data = await con.sendFloat(url,prefix, id, requestKey);
    updateUi(prefix, data);
}

async function toggle(url, prefix, id, requestKey) {
    let data = await con.toggle(url, prefix, id, requestKey);
    updateUi(prefix, data);
}

