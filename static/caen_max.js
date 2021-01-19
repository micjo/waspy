import * as caen from './caen.js'
import * as con from './daemon_connection.js'

export {toggleAcquisition, toggleListData, caenClearData, caenSaveHistogram, caenContinueOnError, caenSaveRegistry, togglePlotHistogram};

let caen1 = new caen.caen('http://ubuntu-desktop:22123');


let ctx = document.getElementById('chart').getContext('2d');
let plotHistogram = false;
let lineChart = new Chart(ctx, {
  type: 'scatter',
  data: {
      labels: [],
      datasets: [{
          label: 'Histogram',
          backgroundColor: 'rgba(242, 207, 222, 0.40)'
      }]
  },
  options: {
    maintainAspectRatio: false,
    animation: {
        duration: 0 // general animation time
    },
    hover: {
        animationDuration: 0 // duration of animations when hovering an item
    },
    elements: {
      line: {
          tension: 0 // disables bezier curves
      }
    },
    responsiveAnimationDuration: 0 // animation duration after a resize
  }
});

async function refreshData() {
    await caen1.updateActuals();
    updateCaen();

    if (plotHistogram) {
        drawGraph();
    }
}

function togglePlotHistogram() {
    console.log("toggle plot histogram");
    plotHistogram = !plotHistogram;
    if (plotHistogram) {
        con.setButtonOn("caen_toggle_plot_histogram");
        con.getEl("caen_toggle_plot_histogram_text").innerText = "Plotting histogram";
        drawGraph();
    }
    else {
        con.setButtonOff("caen_toggle_plot_histogram");
        con.getEl("caen_toggle_plot_histogram_text").innerText = "Not plotting histogram";
    }


}

function drawGraph() {
    console.log("TODO: parse data from caen");
    lineChart.data.datasets[0].label = "Histogram";
    lineChart.data.datasets[0].data = [{x:0,y:10},{x:1,y:11}];
    lineChart.update();
}


function updateCaen() {
    updateAcquireButton();
    updateListDataButton();
    con.getEl("caen_request_id").innerText = caen1.requestId;
    con.getEl("caen_acquiring_data").innerText = caen1.acquiringData;
    con.getEl("caen_storing_list_data").innerText = caen1.listDataSaving;
    con.getEl("caen_histogram_folder").innerText = caen1.histogramLocation;
    con.getEl("caen_list_data_folder").innerText = caen1.listDataLocation;
    con.getEl("caen_list_data_timeout").innerText = caen1.listDataTimeout;
    con.setConnected("caen_connect_status", caen1.connected);
    con.getEl("caen_time").innerText = con.getUniqueIdentifier();

    if (!caen1.requestAcknowledge) {
        con.collapsableError("caen_request_status", "Daemon did not acknowledge request");
        caen1.requestAcknowledge = true;
    }

    con.getEl("caen_error_status").innerHTML='';
    if (caen1.error !== "Success") {
        con.collapsableError("caen_error_status", "Daemon error: " + caen1.error);
        caen1.error = "Success";
    }
}

async function toggleAcquisition() {
    con.show("caen_toggle_acquisition_spinner");
    await caen1.toggleAcquire();
    con.hide("caen_toggle_acquisition_spinner");
    updateCaen();
}

async function toggleListData() {
    let listDataTry = caen1.listDataSaving;
    listDataTry = !listDataTry;
    if (listDataTry){
        let folder = con.getEl("caen_list_data_folder_request").value;
        let timeout = con.getEl("caen_list_data_timeout_request").value;
        if (folder && timeout) {
            con.show("caen_toggle_list_data_spinner");
            await caen1.startStoringListData(folder, timeout);
            con.hide("caen_toggle_list_data_spinner");
        }
        else {
            con.collapsableError("caen_request_status", "To store list data, " +
                "you need to specify folder and timeout.");
        }

    }
    else {
        con.show("caen_toggle_list_data_spinner");
        await caen1.stopStoringListData();
        con.hide("caen_toggle_list_data_spinner");
    }
    updateCaen();
}

async function caenSaveHistogram() {
        let folder = con.getEl("caen_histogram_folder_request").value;
        if(folder) {
            con.show("caen_save_histogram_spinner");
            await caen1.saveHistogram(folder);
            con.hide("caen_save_histogram_spinner");
        }
        else {
            con.collapsableError("caen_request_status", "To store the histograms, " +
                "you need to specify a folder");
        }
}

async function caenClearData() {
    con.show("caen_clear_data_spinner");
    await caen1.clearData();
    con.hide("caen_clear_data_spinner");
}

async function caenContinueOnError() {
    con.show("caen_continue_spinner");
    await caen1.continueOnError();
    con.hide("caen_continue_spinner");
}

async function caenSaveRegistry() {
    con.show("caen_save_registry_spinner");
    await caen1.saveRegistry();
    con.hide("caen_save_registry_spinner");
}

function updateListDataButton() {
    if (caen1.listDataSaving) {
        con.setButtonOn("caen_toggle_list_data");
        con.getEl("caen_toggle_list_data_text").innerText = "Saving list data";
    }
    else {
        con.setButtonOff("caen_toggle_list_data");
        con.getEl("caen_toggle_list_data_text").innerText = "Not saving list data";

    }
}

function updateAcquireButton() {
    if (caen1.acquiringData) {
        con.setButtonOn("caen_toggle_acquisition");
        con.getEl("caen_toggle_acquisition_text").innerText = "Acquiring data";
    }
    else {
        con.setButtonOff("caen_toggle_acquisition");
        con.getEl("caen_toggle_acquisition_text").innerText = "Not acquiring data";
    }
}

window.setInterval(function() {
    refreshData();
}, 2000);

