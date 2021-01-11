export {sendRequest, getUniqueIdentifier, collapsableError, collapsableSucess, collapsableNotify}
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

function postData(host, textBody)
{
    fetch(host, {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain',
        },
        body: textBody
    });
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


function getCompletionTime(url, requestId, retryLimit, retryCount) {
    return fetch(url)
        .then (response => response.json())
        .then (data => {
            console.log(data);
            if ( data["request_id"] === requestId) {
                console.log("match");
                console.log(data);
                return data["expiry_date"];
            }
            else if (retryCount < retryLimit) {
                return delay(100).then(() => getCompletionTime(url, requestId, retryLimit, retryCount+1));
            }
        });
}

async function sendRequest(url, requestId, request, statusId) {
    postData(url+"/engine", request);
    let expiry_date = await getCompletionTime(url+"/actuals", requestId, 10, 0);
    if (expiry_date === undefined) {
        collapsableError(statusId, "Failed to send request");
    }
    else {
        collapsableSucess(statusId, "Request sent, should be done at: " + expiry_date);
    }
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
    getEl(id).innerHTML = "";
    let errorDiv = makeAlert("alert-danger", message);
    document.getElementById(id).appendChild(errorDiv);
}

function collapsableSucess(id, message) {
    getEl(id).innerHTML = "";
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
