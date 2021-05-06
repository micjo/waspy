import * as con from './daemon_connection.js'

export {refreshGraph};

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
