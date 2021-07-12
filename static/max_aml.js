import * as con from './daemon_connection.js'

export {
    load,
    submit,
    updateUi,
    sendARequest,
    sendInt,
    sendString,
    sendFloat,
    toggle,
    refreshData,
    refreshDataRepeatedly
}

function refreshDataRepeatedly(url, prefix, timeout) {
    refreshData(url, prefix);
    window.setInterval(function() {
        refreshData(url,prefix);
    }, timeout);
}

async function refreshData(url,prefix) {
    let hwData = await con.getStatus(url)
    updateUi(prefix, hwData);
}



function updateUi(prefix, hwData) {
    con.setSanityBadge(prefix, hwData);
    if (!hwData) {return;}

    con.setElementText(prefix + '_request_id', hwData["request_id"]);
    con.setElementText(prefix + '_request_finished', hwData["request_finished"]);
    con.setElementText(prefix + '_expiry', hwData["expiry_date"]);
    con.setElementText(prefix + '_error', hwData["error"]);
    con.setElementText(prefix + '_first_temperature', hwData["motor_1_temperature"]);
    con.setElementText(prefix + '_first_step', hwData["motor_1_steps"]);
    con.setElementText(prefix + '_first_offset', hwData["motor_1_offset"]);
    con.setElementText(prefix + '_update_m1_position', hwData["motor_1_updating_position"]);
    con.setElementText(prefix + '_update_m1_temperature', hwData["motor_1_updating_temperature"]);
    con.setElementText(prefix + '_second_temperature', hwData["motor_2_temperature"]);
    con.setElementText(prefix + '_second_step', hwData["motor_2_steps"]);
    con.setElementText(prefix + '_second_offset', hwData["motor_2_offset"]);
    con.setElementText(prefix + '_update_m2_position', hwData["motor_2_updating_position"]);
    con.setElementText(prefix + '_update_m2_temperature', hwData["motor_2_updating_temperature"]);
    con.setElementText(prefix + '_debug_rs232', hwData["debug_rs232"]);
    con.setElementText(prefix + '_debug_aml', hwData["debug_aml"]);
    con.setElementText(prefix + '_debug_broker', hwData["debug_broker"]);

    con.setElementChecked(prefix + "_update_m1_position_click", hwData["motor_1_updating_position"]);
    con.setElementChecked(prefix + "_update_m1_temperature_click", hwData["motor_1_updating_temperature"]);
    con.setElementChecked(prefix + "_debug_rs232_click", hwData["debug_rs232"]);
    con.setElementChecked(prefix + "_debug_aml_click", hwData["debug_aml"]);
    con.setElementChecked(prefix + "_debug_broker_click", hwData["debug_broker"]);

    let position_str = parseFloat(hwData["motor_1_position"]).toFixed(2);
    position_str += ", " + parseFloat(hwData["motor_2_position"]).toFixed(2);
    con.setElementText(prefix + "_brief_status", position_str);

    if (hwData["request_finished"]) {
        con.hide(prefix + "_moving_status");
        con.setElementText(prefix + '_first_position', hwData["motor_1_position"]);
        con.setElementText(prefix + '_adv_first_position', hwData["motor_1_position"]);
        con.setElementText(prefix + '_second_position', hwData["motor_2_position"]);
        con.setElementText(prefix + '_adv_second_position', hwData["motor_2_position"]);
        con.setElementText(prefix + '_first', hwData["motor_1_position"]);
        con.setElementText(prefix + '_second', hwData["motor_2_position"]);
        con.setBadgeType(prefix + "_brief_status", "bg-success");
    }

    else {
        con.show(prefix + "_moving_status");
        con.setElementText(prefix + '_first_position', "-");
        con.setElementText(prefix + '_adv_first_position', "-");
        con.setElementText(prefix + '_second_position', "-");
        con.setElementText(prefix + '_adv_second_position', "-");
        con.setElementText(prefix + '_first', "-");
        con.setElementText(prefix + '_second', "-");
        con.setBadgeType(prefix + "_brief_status", "bg-secondary");
        
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
    console.log(firstPos);
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

