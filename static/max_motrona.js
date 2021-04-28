import * as con from './daemon_connection.js'

export {
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

    con.getEl(prefix + '_request_id').innerText = hwData["request_id"];
    con.getEl(prefix + '_request_finished').innerText = hwData["request_finished"];
    con.getEl(prefix + '_target_charge').innerText = hwData["target_charge(nC)"];
    con.getEl(prefix + '_counts').innerText = hwData["counts"];
    con.getEl(prefix + '_status').innerText = hwData["status"];
    con.getEl(prefix + '_charge').innerText = hwData["charge(nC)"];
    con.updateElement(prefix + '_counting_time', hwData["counting_time(msec)"]);
    con.updateElement(prefix + '_current', hwData["current(nA)"]);
    con.updateElement(prefix + '_error', hwData["error"]);

    if (maxMode) {
        con.updateElement(prefix + '_pulse_to_counts', hwData["counter_factor"]);
        con.updateElement(prefix + '_analog_end', hwData["analog_end"]);
        con.updateElement(prefix + '_analog_start', hwData["analog_start"]);
        con.updateElement(prefix + '_analog_offset', hwData["analog_offset"]);
        con.updateElement(prefix + '_analog_gain', hwData["analog_gain"]);
        con.updateElement(prefix + '_preselection_1', hwData["preselection_1"]);
        con.updateElement(prefix + '_preselection_2', hwData["preselection_2"]);
        con.updateElement(prefix + '_preselection_3', hwData["preselection_3"]);
        con.updateElement(prefix + '_preselection_4', hwData["preselection_4"]);
        con.updateElement(prefix + '_target_counts', hwData["target_counts"]);
        con.updateElement(prefix + '_firmware_version', hwData["firmware_version"]);
        con.updateElement(prefix + '_counts_to_charge', hwData["nc_to_pulses_conversion_factor"]);
        con.updateElement(prefix + '_count_mode', hwData["count_mode"]);
        con.updateElement(prefix + '_input_pulse_type', hwData["input_pulse_type"]);
        con.updateElement(prefix + '_debug_rs232', hwData["debug_rs232"]);
        con.updateElement(prefix + '_debug_motrona', hwData["debug_motrona"]);
        con.updateElement(prefix + '_debug_broker', hwData["debug_broker"]);
        con.getEl(prefix + "_debug_rs232").checked = hwData["debug_rs232"];
        con.getEl(prefix + "_debug_motrona").checked = hwData["debug_motrona"];
        con.getEl(prefix + "_debug_broker").checked = hwData["debug_broker"];
    }
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
