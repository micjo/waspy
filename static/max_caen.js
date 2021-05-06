import * as con from './daemon_connection.js'
export {
    updateUi,
    sendARequest,
    sendInt,
    sendString,
    sendFloat,
    toggle,
    refreshData,
    refreshDataRepeatedly,
    drawGraph
}

async function drawGraph(url) {
    if (!con.getEl("update_graph_request").checked) {
        return;
    }

    let board = con.getEl("board_select").value;
    let channel = con.getEl("channel_select").value;
    let fullPath = url + "/histogram/" + board + "-" + channel;
    console.log(fullPath);

    fetch(url + "/histogram/" + board + "-" + channel)
        .then(response => {
            if(response.status === 404) {
                throw "Failed to retrieve data. Does this board + channel exist?";
            }
            return response.text()
        }
        )
        .then(data => {
            let x_values = [];
            let y_values = [];
            let i = 0;
            for (const datapoint of data.split(";")) {
                x_values.push(i);
                y_values.push(parseInt(datapoint));
                i++;
            }

            const plotdata = [{
                x: x_values,
                y: y_values,
                type: 'scatter'
            }];

            const layout = {
              title: 'histogram',
              uirevision: 'test',
              autosize:'true',
              height:300
            };

            Plotly.newPlot('histo_chart', plotdata, layout);
        })
        .catch(error => {
            con.showFailureModal(error);
            con.getEl("update_graph_request").checked = false;
        });
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
    con.setElementText(prefix + '_acquiring', hwData["acquisition_active"]);
    con.setElementText(prefix + '_brief_status', "Acquiring: " + hwData["acquisition_active"]);

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
