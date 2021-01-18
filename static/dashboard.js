import * as aml from './aml.js'
import * as caen from './caen.js'

let caen1 = new caen.caen('http://ubuntu-desktop:22123', 'caen');

function refreshData() {
    console.log("refreshing");
    caen1.updateActuals();
}

window.setInterval(function() {
    refreshData();
}, 2000);
