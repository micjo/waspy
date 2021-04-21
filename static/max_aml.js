import * as con from './controllers/daemon_connection.js'

export {refreshAllData, setMinMode};
export {
    sendInt,
    sendFloat,
    sendString,
    sendARequest,
    submit,
    load,
    toggle
}



async function refreshAllData(url, prefix) {
    let hwData = await con.getStatus(url)

    if (hwData) {
        con.setConnected(prefix + "_connect_status", true);
        updateUi(prefix, hwData);
    }
    else {
        con.setConnected(prefix + "_connect_status", false);
    }
}

let minMode = false;


function setMinMode() {
    minMode = true;
}

function updateElement(id, value) {
    if (value === undefined) {
        con.getEl(id).innerText = "-";
    }
    else if (value === "") {
        con.getEl(id).innerText = "-";
    }
    else {
        con.getEl(id).innerText = value;
    }
}

function updateUi(prefix, hwData) {

    updateElement(prefix + '_request_id', hwData["request_id"]);
    updateElement(prefix + '_request_finished', hwData["request_finished"]);
    updateElement(prefix + '_error', hwData["error"]);
    updateElement(prefix + '_first', hwData["motor_1_position"]);
    updateElement(prefix + '_second', hwData["motor_2_position"]);

    if (!minMode) {
        updateElement(prefix + '_first_position', hwData["motor_1_position"]);
        updateElement(prefix + '_first_temperature', hwData["motor_1_temperature"]);
        updateElement(prefix + '_first_step', hwData["motor_1_steps"]);
        updateElement(prefix + '_first_offset', hwData["motor_1_offset"]);
        updateElement(prefix + '_update_m1_position', hwData["motor_1_updating_position"]);
        updateElement(prefix + '_update_m1_temperature', hwData["motor_1_updating_temperature"]);

        updateElement(prefix + '_second_position', hwData["motor_2_position"]);
        updateElement(prefix + '_second_temperature', hwData["motor_2_temperature"]);
        updateElement(prefix + '_second_step', hwData["motor_2_steps"]);
        updateElement(prefix + '_second_offset', hwData["motor_2_offset"]);
        updateElement(prefix + '_update_m2_position', hwData["motor_2_updating_position"]);
        updateElement(prefix + '_update_m2_temperature', hwData["motor_2_updating_temperature"]);

        updateElement(prefix + '_debug_rs232', hwData["debug_rs232"]);
        updateElement(prefix + '_debug_aml', hwData["debug_aml"]);
        updateElement(prefix + '_debug_broker', hwData["debug_broker"]);
        con.getEl(prefix + "_update_m1_position_request").checked = hwData["motor_1_updating_position"];
        con.getEl(prefix + "_update_m1_temperature_request").checked = hwData["motor_1_updating_temperature"];
        con.getEl(prefix + "_debug_rs232").checked = hwData["debug_rs232"];
        con.getEl(prefix + "_debug_aml").checked = hwData["debug_aml"];
        con.getEl(prefix + "_debug_broker").checked = hwData["debug_broker"];
    }

}


async function toggle(url, prefix, id, requestKey) {
    let value = con.getEl(prefix + "_" +id + "_request").checked;
    let request = {};
    request[requestKey] = value;
    await sendRequest(url,prefix, prefix +"_" +id + "_spinner", request);
}

async function sendRequest(url, prefix, spinner, request ) {
    let hwData = await con.sendRequestAndSpin(url, request, spinner);
    updateUi(prefix, hwData);
}

function submit(url, prefix, id) {
    let pos1 = parseFloat(con.getEl(prefix + "_first_request").value);
    let pos2 = parseFloat(con.getEl(prefix + "_second_request").value);

    if (isNaN(pos1)|| isNaN(pos2)) {
        alert('invalid input');
        return;
    }

    let request = {};
    request["set_m1_target_position"] = pos1;
    request["set_m2_target_position"] = pos2;
    sendRequest(url, prefix, prefix + "_" + id + "_spinner", request);
}

function load(prefix, firstPos, secondPos){
    con.getEl(prefix + "_first_request").value = firstPos;
    con.getEl(prefix + "_second_request").value = secondPos;
}



function sendARequest(url, prefix, id ,request) {
    let jsonRequest =  JSON.parse(request);
    sendRequest(url,prefix, prefix +"_" +id + "_spinner", jsonRequest);
}

function sendInt(url,prefix, id, requestKey) {
    let value = parseInt(con.getEl(prefix + "_" +id + "_request").value);
    if (!Number.isInteger(value)) {
        alert("This is not a valid integer number");
        return;
    }
    let request = {};
    request[requestKey] = value;
    sendRequest(url,prefix, prefix +"_" +id + "_spinner", request);
}

function sendString(url,prefix, id, requestKey) {
    let value = con.getEl(prefix + "_" +id + "_request").value;
    if (value === "Choose...") { return; }
    let request = {};
    request[requestKey] = value;
    sendRequest(url,prefix, prefix +"_" +id + "_spinner", request);
}

function sendFloat(url,prefix, id, requestKey) {
    let value = parseFloat(con.getEl(prefix + "_" +id + "_request").value);
    if (isNaN(value)) {
        alert("This is not a valid floating point number");
        return;
    }
    let request = {};
    request[requestKey] = value;
    sendRequest(url,prefix, prefix +"_" +id + "_spinner", request);
}
