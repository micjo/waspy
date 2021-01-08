export {sendRequest, getUniqueIdentifier, collapsableError, collapsableSucess, collapsableNotify}
export {checkErrorClear}
export {checkRequest}
export {getEl}
export {motors,dataAcq}

let motors = {
    xyUrl : 'http://localhost:22000',
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

function sendRequest(host, textBody, statusId)
{
    collapsableNotify(statusId, "Sending Request");
    fetch(host, {
    method: 'POST',
    headers: {
      'Content-Type': 'text/plain',
    },
    body: textBody
  })
  .then(response => {
      if (!response.ok) {
        throw new Error(response.text());
      }
      collapsableSucess(statusId, "Request received");
  })
  .catch(error => {
      collapsableError(statusId, error);
  });
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


function fetchWithRetry(url, id, retryLimit, retryCount) {
    console.log("fetching id with retry");
    return fetch(url)
        .then( response => response.json())
        .then (data => {
            console.log(data);
            if ( data["request_id"] === id) {
                console.log("match with pass");
                return data;
            }
            else if ( data["error_status"] !== "Success") {
                console.log("match with fail");
                return data;
            }
            else if (retryCount < retryLimit ) {
                return delay(100).then(() => fetchWithRetry(url, id, retryLimit, retryCount + 1));
            }
        });
}

function fetchDoneWithRetry(url, id, statusId, retryLimit, retryCount) {
    console.log("fetching done with retry");
    return fetch(url)
        .then( response => response.json())
        .then (data => {
            console.log(data);
            if ( data["status"] === "Done" && data["request_id"] === id) {
                console.log("done with request");
                collapsableSucess("The motor has arrived");
                return data;
            }
            else if ( data["error_status"] !== "Success") {
                console.log("match with fail");
                collapsableError(data["error_status"]);
                return data;
            }
            else if (retryCount < retryLimit ) {
                console.log("are we there yet");
                return delay(1000).then(() => fetchDoneWithRetry(url, id, statusId, retryLimit, retryCount + 1));
            }
        });
}


function checkErrorClear(url, statusId, retryLimit, retryCount) {
    return fetch(url)
        .then( response => response.json())
        .then (data => {
            console.log(data);
            if ( data["error_status"] === "Success" ) {
                console.log("error cleared");
                collapsableSucess(statusId, "Error cleared");
                return data;
            }
            else if (retryCount < retryLimit ) {
                return delay(100).then(() => fetchWithRetry(url, id, retryLimit, retryCount + 1));
            }
            else {
                collapsableError(statusId, "Could not clear error");
            }
        });
}


function checkRequest(host, id, statusId)
{
    console.log("checking with id: " + id );
    fetchWithRetry(host, id, 30, 0)
        .then(data => {
            console.log(data);
            if ( data["error_status"] === "Success") {
                collapsableSucess(statusId, "Request parsed and executing");
            }
            else {
                collapsableError(statusId, data["error_status"]);
            }
        })
        .then(fetchDoneWithRetry(host, id, statusId, 30, 0))
        .catch( error => {
            collapsableError(statusId, error);
        });

}

function getUniqueIdentifier() {
    let timestamp = new Date(Date.now()).toLocaleTimeString("nl-BE");
    return  timestamp;
}

function collapsableNotify(id,message) {
    let notifyDiv = makeAlert("alert-secondary", message);
    document.getElementById(id).appendChild(notifyDiv);
    setTimeout(function() {
        document.getElementById(id).removeChild(notifyDiv);
    }, 5000);
}

function collapsableError(id, message) {
    let errorDiv = makeAlert("alert-danger", message);
    document.getElementById(id).appendChild(errorDiv);
}

function collapsableSucess(id, message) {
    let successDiv = makeAlert("alert-success", message);
    document.getElementById(id).appendChild(successDiv);
    setTimeout(function() {
        document.getElementById(id).removeChild(successDiv);
    }, 5000);
}

function makeAlert(alertType, message) {
    let alertDiv = document.createElement('div');
    alertDiv.classList.add("alert", alertType, "alert-dismissible", "top-margin");
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
