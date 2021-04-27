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

}

