import * as con from './daemon_connection.js'

export {refreshGraph, refreshData, refreshDataRepeatedly, abort, pause, resume};

function refreshDataRepeatedly(timeout) {
    refreshData("/api/rbs/state");
    window.setInterval(function() {
        refreshData("/api/rbs/state");
    }, timeout);
}

async function refreshData(url) {
    let hwData = await con.getStatus(url)
    updateUi(hwData);
}

async function abort() {
    con.postData("/api/rbs/abort", "");
}

async function pause() {
    let request = { "pause_dir_scan": true};
    await con.postData("/api/rbs/pause_dir_scan", JSON.stringify(request));
}

async function resume() {
    let request = { "pause_dir_scan": false };
    await con.postData("/api/rbs/pause_dir_scan", JSON.stringify(request));
}

function updateUi(hwData) {

    con.getEl("rbs_status").innerHTML = "";
    con.setElementText("rbs_brief_status", hwData["status"]);
    if (hwData["status"] == "Idle") {
        return;
    }

    for (const scene of hwData["experiment"]["scenario"]) {
        let sceneRow = document.createElement("tr");

        let sceneTitle = document.createElement("td");
        sceneTitle.innerText = scene["ftitle"]

        let xPos = document.createElement("td");
        xPos.innerText = scene["x"]

        let yPos = document.createElement("td");
        yPos.innerText = scene["y"]

        let sceneStatus = document.createElement("td");
        sceneStatus.innerText = scene["execution_state"]

        let sceneProgress = document.createElement("td");
        let ratio = scene["phi_progress"]
        if (ratio != undefined) {
            let progress = document.createElement("div");
            progress.setAttribute("class", "progress");
            let progressBar = document.createElement("div");
            progressBar.setAttribute("class", "progress-bar");
            progressBar.setAttribute("style", "width: "+ ratio+ "%;");
            progressBar.innerText = ratio + "%";
            progress.appendChild(progressBar);
            sceneProgress.appendChild(progress);
        }

        sceneRow.appendChild(sceneTitle);
        sceneRow.appendChild(xPos);
        sceneRow.appendChild(yPos);
        sceneRow.appendChild(sceneStatus);
        sceneRow.appendChild(sceneProgress);

        con.getEl("rbs_status").appendChild(sceneRow);

    }

}

function refreshGraph() {
    if (!con.getEl("update_rbs_request").checked) {
        return;
    }

    fetch("http://localhost:5000/trends/rbs_current")
        .then(response => response.json())
        .then(data => {

            let x_values = [];
            let y_values = [];
            for (const datapoint of data) {
                x_values.push(datapoint[0]);
                y_values.push(datapoint[1]);
            }

            const plotdata = [{
                x: x_values,
                y: y_values,
                type: 'scatter'
            }];

            const layout = {
              title: 'Motrona RBS current',
              uirevision: 'test',
              autosize:'true',
              height:300
            };

            Plotly.newPlot('rbs_current', plotdata, layout);
            });

    fetch("http://localhost:5000/trends/aml_positions")
        .then(response => response.json())
        .then(data => {

            let x_values = [];
            let y_values = [];
            for (const datapoint of data) {
                x_values.push(datapoint[0]);
                y_values.push(datapoint[1]);
            }

            const plotdata = [{
                x: x_values,
                y: y_values,
                type: 'scatter'
            }];

            const layout = {
              title: 'AML X position',
              uirevision: 'test',
              autosize:'true',
              height:300
            };

            Plotly.newPlot('motor_pos_graph', plotdata, layout);
            });
}
