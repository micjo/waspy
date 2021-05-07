import * as con from './daemon_connection.js'

export {refreshGraph, refreshData, refreshDataRepeatedly};

function refreshDataRepeatedly(timeout) {
    refreshData("/api/exp/rbs");
    window.setInterval(function() {
        refreshData("/api/exp/rbs");
    }, timeout);
}

async function refreshData(url) {
    let hwData = await con.getStatus(url)
    updateUi(hwData);
}

function updateUi(hwData) {
    con.getEl("rbs_status").innerHTML = "";
    if (hwData["experiment"] !== undefined) {
        con.setElementText("rbs_brief_status", "Experiment Ongoing");
    }
    else {
        con.setElementText("rbs_brief_status", "Idle");
        return;
    }

    for (const scene of hwData["experiment"]) {
        console.log(scene);
        let sceneRow = document.createElement("tr");

        let sceneTitle = document.createElement("td");
        sceneTitle.innerText = scene["ftitle"]

        let sceneStatus = document.createElement("td");
        sceneStatus.innerText = scene["execution_state"]

        let sceneProgress = document.createElement("td");
        let ratio = ((scene["phi_progress"] / hwData["phi_end"]) * 100).toFixed(0);
        if (ratio != "NaN") {
            console.log(ratio);
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
