export {sendRequest, getUniqueIdentifier, collapsableError, collapsableSucess, collapsableNotify}
export {getEl}
export {motors,dataAcq}

let motors = {
    xy : {
        responseUrl : 'http://localhost:22000/actuals',
        requestUrl : 'http://localhost:22000/engine'
    },
    detTheta : {
        responseUrl : 'http://localhost:22001/actuals',
        requestUrl : 'http://localhost:22001/engine'
    },
    phiZeta : {
        responseUrl : 'http://localhost:22002/actuals',
        requestUrl : 'http://localhost:22002/engine'
    }
};

let dataAcq = {
    caen : {
        responseUrl : 'http://localhost:22003/actuals',
        requestUrl : 'http://localhost:22003/engine'
    }
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
