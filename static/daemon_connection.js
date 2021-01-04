export {aml_xy_response, aml_det_response, aml_phi_response, caen_host_1_response}
export {aml_xy_request, aml_det_request, aml_phi_request, caen_host_1_request}
export {sendRequest, getUniqueIdentifier, collapsableError, collapsableSucess, collapsableNotify}
export {MotorIndex}
export {getEl}

let aml_host = 'http://localhost'
let caen_host = 'http://localhost'

let aml_xy = aml_host + ":22000"
let aml_det = aml_host + ":22001"
let aml_phi = aml_host + ":22002"
let caen_host_1 = caen_host + "22003"

let aml_xy_response = aml_xy + "/actuals"
let aml_det_response = aml_det + "/actuals"
let aml_phi_response = aml_phi + "/actuals"
let caen_host_1_response = caen_host_1 + "/actuals"

let aml_xy_request = aml_xy + "/engine"
let aml_det_request = aml_det + "/engine"
let aml_phi_request = aml_phi + "/engine"
let caen_host_1_request = caen_host_1 + "/engine"

const MotorIndex = {
    FIRST: "first",
    SECOND: "second"
}

function sendRequest(host, textBody)
{
    collapsableNotify("#collapseExample", "Sending Request");
    fetch(host, {
    method: 'POST',
    headers: {
      'Content-Type': 'text/plain',
    },
    body: textBody
  })
  .then(response => {
      if (!response.ok) {
        throw new Error('Malformed request');
      }
      collapsableSucess('#collapseExample', "Request received");
  })
  .catch((error) => {
      collapsableError("#collapseExample", error);
  });
}

function getUniqueIdentifier() {
    let timestamp = new Date(Date.now()).toLocaleTimeString("nl-BE");
    return  "request_id="+timestamp + "\n";
}

function collapsableNotify(id,message) {
    let notifyDiv = makeAlert("alert-secondary", message);
    $(id).empty();
    $(id).append(notifyDiv);
    $(id).collapse('show');
}

function collapsableError(id, message) {
    let errorDiv = makeAlert("alert-danger", message);
    $(id).empty();
    $(id).append(errorDiv);

    $(id).collapse('show');
    setTimeout(function() {
        $(id).collapse('hide');
    }, 5000);
}

function collapsableSucess(id, message) {
    let successDiv = makeAlert("alert-success", message);
    $(id).empty();
    $(id).append(successDiv);
    $(id).collapse('show');

    setTimeout(function() {
        $(id).collapse('hide');
    }, 2000);
}

function makeAlert(alertType, message) {
    let alertDiv = document.createElement('div');
    alertDiv.classList.add("alert", alertType, "alert-dismissible","fade","show", "top-margin");
    alertDiv.setAttribute("role", "alert");
    alertDiv.innerText = message;
    let closeDiv = document.createElement("button");
    closeDiv.classList.add("close");
    closeDiv.setAttribute("data-dismiss", "alert");
    let spanDiv = document.createElement("span");
    spanDiv.setAttribute("aria-hidden","true");
    spanDiv.innerHTML = "&times";
    closeDiv.append(spanDiv);
    alertDiv.append(closeDiv);

    return alertDiv;
}

function getEl(element) {
    return document.getElementById(element);
}
