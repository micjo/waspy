import * as con from './daemon_connection.js'

export {
    refreshAllData
};


async function refreshAllData(rbs_config) {

    for (const key in rbs_config) {
        let hwData = await con.getStatus("/api/" + key);

        if (hwData === "") {
            con.setElementText(key + "_connect_state", "Disconnected");
            con.setElementText(key + "_error_state", "-");
            con.setElementText(key + "_request_id", "-");
            con.setBadgeDanger(key + "_connect_state");
            con.setElementText(key + "_status", "-");
        }
        else {
            con.setElementText(key + "_connect_state", "Connected");
            con.setElementText(key + "_error_state", hwData["error"]);
            con.setElementText(key + "_request_id", hwData["request_id"]);
            con.setBadgeSuccess(key + "_connect_state");
            con.setBadgeError(key + "_error_state", hwData["error"] !== "Success");

            if (rbs_config[key]["type"] == "aml") {
                con.setElementText(key + "_status", "Busy: " + hwData["busy"]);
            }
            if (rbs_config[key]["type"] == "motrona") {
                con.setElementText(key + "_status", "Status: " + hwData["status"]);
            }
            if (rbs_config[key]["type"] == "caen") {
                con.setElementText(key + "_status", "Acquiring Data: " + hwData["acquisition_active"]);
            }

        }

    }
}
