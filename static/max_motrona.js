import * as con from './controllers/daemon_connection.js'

export {refreshAllData, sendRequest}

async function refreshAllData(url, prefix) {

    //let hwData = await con.getStatus(url);
    //updateUi(prefix, hwData);
}


async function sendRequest(url, prefix, spinner, request ) {
    let hwData = await con.sendRequestAndSpin(url, JSON.parse(request), spinner);
    console.log(hwData);
    updateUi(prefix, hwData);
}

function updateUi(prefix, hwData) {
    con.getEl(prefix + '_request_id').innerText = hwData["request_id"];
    con.getEl(prefix + '_request_finished').innerText = hwData["request_finished"];
    con.getEl(prefix + '_target_charge').innerText = hwData["target_charge(nC)"];

}

function test() {
    console.log("inside max motrona");
    return {'target_charge' : 13};
}
