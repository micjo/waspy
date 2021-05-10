import * as con from './daemon_connection.js'

export {
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
    if (!hwData) {
        con.setBadgeErrorWithText(prefix + "_connect_status" , false, "Not Active");
        return;
    }
    con.setBadgeErrorWithText(prefix + "_connect_status" , true, "Active");

    con.setElementText(prefix + '_request_id', hwData["request_id"]);
    con.setElementText(prefix + '_request_finished', hwData["request_finished"]);
    con.setElementText(prefix + '_target_charge', hwData["target_charge(nC)"]);
    con.setElementText(prefix + '_counts', hwData["counts"]);
    con.setElementText(prefix + '_status', hwData["status"]);
    con.setElementText(prefix + '_charge', hwData["charge(nC)"]);
    con.setElementText(prefix + '_counting_time', hwData["counting_time(msec)"]);
    con.setElementText(prefix + '_current', hwData["current(nA)"]);
    con.setElementText(prefix + '_error', hwData["error"]);
    con.setElementText(prefix + '_pulse_to_counts', hwData["counter_factor"]);
    con.setElementText(prefix + '_analog_end', hwData["analog_end"]);
    con.setElementText(prefix + '_analog_start', hwData["analog_start"]);
    con.setElementText(prefix + '_analog_offset', hwData["analog_offset"]);
    con.setElementText(prefix + '_analog_gain', hwData["analog_gain"]);
    con.setElementText(prefix + '_preselection_1', hwData["preselection_1"]);
    con.setElementText(prefix + '_preselection_2', hwData["preselection_2"]);
    con.setElementText(prefix + '_preselection_3', hwData["preselection_3"]);
    con.setElementText(prefix + '_preselection_4', hwData["preselection_4"]);
    con.setElementText(prefix + '_target_counts', hwData["target_counts"]);
    con.setElementText(prefix + '_firmware_version', hwData["firmware_version"]);
    con.setElementText(prefix + '_counts_to_charge', hwData["nc_to_pulses_conversion_factor"]);
    con.setElementText(prefix + '_count_mode', hwData["count_mode"]);
    con.setElementText(prefix + '_input_pulse_type', hwData["input_pulse_type"]);
    con.setElementText(prefix + '_debug_rs232', hwData["debug_rs232"]);
    con.setElementText(prefix + '_debug_motrona', hwData["debug_motrona"]);
    con.setElementText(prefix + '_debug_broker', hwData["debug_broker"]);
    con.setElementChecked(prefix + "_debug_rs232", hwData["debug_rs232"]);
    con.setElementChecked(prefix + "_debug_motrona", hwData["debug_motrona"]);
    con.setElementChecked(prefix + "_debug_broker", hwData["debug_broker"]);

    if (hwData["status"] === "Counting") {
        con.show(prefix + "_counting_status");
    }
    else {
        con.hide(prefix + "_counting_status");
    
    }

    let brief_str = "Counting: " + hwData["status"] + ", Charge: "
    brief_str += parseFloat(hwData["charge(nC)"]).toFixed(2);
    brief_str += " -> "
    brief_str += parseFloat(hwData["target_charge(nC)"]).toFixed(2);
    con.setElementText(prefix + '_brief_status', brief_str);
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
