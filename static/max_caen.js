import * as con from './daemon_connection.js'
export {
    updateUi,
    setMaxMode,
    sendARequest,
    sendInt,
    sendString,
    sendFloat,
    toggle,
    refreshData,
    drawGraph
}

let maxMode = false;

function setMaxMode() {
    maxMode = true;
}

async function drawGraph() {
    fetch("http://olympus:22000/api/histogram/1/0")
        .then(response => response.text())
        .then(data => {
            let x_values = [];
            let y_values = [];
            let i = 0;
            for (const datapoint of data.split(";")) {
                x_values.push(i);
                y_values.push(parseInt(datapoint));
                i++;
            }

            const plotData = [{
                x: x_values,
                y: y_values,
                type: 'scatter'
            }];

            const layout = {
              title: 'histogram',
            };

            Plotly.newPlot('histo_chart', plotData, layout);
        });
}

async function refreshData(url,prefix) {
    drawGraph();
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
    con.updateElement(prefix + '_acquiring', hwData["acquisition_active"]);

    if (maxMode) {
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
