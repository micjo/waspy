import * as con from './daemon_connection.js'

export {
    refreshAllData
};


async function refreshAllData(rbs_config) {

    for (const aml of rbs_config["aml"]) {
        let hwData = await con.getStatus("/api/" + aml["id"]);

        if (hwData === "") {
            con.getEl(aml["id"] + "_connect_state").innerText = "Disconnected";
            con.setBadgeDanger(aml["id"] + "_connect_state");
            con.getEl(aml["id"] + "_error_state").innerText = "-";
            con.getEl(aml["id"] + "_request_id").innerText = "-";
            con.getEl(aml["id"] + "_busy").innerText = "-";
        }
        else {
            con.setText(aml["id"] + "_connect_state", "Connected");
            con.setBadgeSuccess(aml["id"] + "_connect_state");
            con.setText(aml["id"] + "_error_state", hwData["error"]);
            con.setBadgeState(aml["id"] + "_error_state", hwData["error"] !== "Success");
            con.setText(aml["id"] + "_request_id", hwData["request_id"]);
            con.setText(aml["id"] + "_busy", "busy: " + hwData["busy"]);
        }
    }

    for (const motrona of rbs_config["motrona"]) {
        let hwData = await con.getStatus("/api/" + motrona["id"]);

        if (hwData === "") {
            con.getEl(motrona["id"] + "_connect_state").innerText = "Disconnected";
            con.setBadgeDanger(motrona["id"] + "_connect_state");
            con.getEl(motrona["id"] + "_error_state").innerText = "-";
            con.getEl(motrona["id"] + "_request_id").innerText = "-";
            con.getEl(motrona["id"] + "_status").innerText = "-";
        }
        else {
            con.setText(motrona["id"] + "_connect_state", "Connected");
            con.setBadgeSuccess(motrona["id"] + "_connect_state");
            con.setText(motrona["id"] + "_error_state", hwData["error"]);
            con.setBadgeState(motrona["id"] + "_error_state", hwData["error"] !== "Success");
            con.setText(motrona["id"] + "_request_id", hwData["request_id"]);
            con.setText(motrona["id"] + "_status", "Status: " + hwData["status"]);
        }
    }

    for (const caen of rbs_config["caen"]) {
        let hwData = await con.getStatus("/api/" + caen["id"]);

        if (hwData === "") {
            con.getEl(caen["id"] + "_connect_state").innerText = "Disconnected";
            con.setBadgeDanger(caen["id"] + "_connect_state");
            con.getEl(caen["id"] + "_error_state").innerText = "-";
            con.getEl(caen["id"] + "_request_id").innerText = "-";
            con.getEl(caen["id"] + "_status").innerText = "-";
        }
        else {
            con.setText(caen["id"] + "_connect_state", "Connected");
            con.setBadgeSuccess(caen["id"] + "_connect_state");
            con.setText(caen["id"] + "_error_state", hwData["error"]);
            con.setBadgeState(caen["id"] + "_error_state", hwData["error"] !== "Success");
            con.setText(caen["id"] + "_request_id", hwData["request_id"]);
            con.setText(caen["id"] + "_status", "Acquiring data: " + hwData["acquisition_active"]);
        }
    }

}

