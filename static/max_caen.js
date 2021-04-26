import * as con from './controllers/daemon_connection.js'

export {refreshAllData, setMinMode};
export {
    sendInt,
    sendFloat,
    sendString,
    sendARequest,
    toggle,
    drawGraph
};



async function drawGraph() {
    if (!con.getEl("graph_update").checked) {
        console.log("update not requested, exit");
        return;
    }


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


async function refreshAllData(url, prefix) {
    drawGraph();
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
    updateElement(prefix + '_acquiring', hwData["acquisition_active"]);

    if (!minMode) {
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
