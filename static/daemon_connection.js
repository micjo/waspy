export {
    collapsableError,
    collapsableNotify,
    collapsableSucess,
    getUniqueIdentifier,
    sendRequestWithExpiryDate
};

export {getEl};
export {dataAcq, motors};
export {getAmlActuals};
export {setButtonOnOrOff};
export {getCaenActuals};

export {toggleCaenListDataState, toggleCaenAcquisitionState};

let motors = {
    xyUrl: 'http://169.254.166.218:22800',
    detThetaUrl: 'http://169.254.166.218:22802',
    phiZetaUrl: 'http://169.254.166.218:22801'
};

let dataAcq =
    {caenUrl: 'http://ubuntu-desktop:22123'}

function postData(host, textBody) {
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

function updateSpinnerVisbility(elementId, data) {
    if (data['status'] === 'Processing') {
        getEl(elementId).style.display = 'block';
    } else if (data['status'] === 'Done') {
        getEl(elementId).style.display = 'none';
    }
}

function setConnected(id, connected) {
    if (connected) {
        document.getElementById(id).innerText = 'Connected';
        document.getElementById(id).setAttribute(
            'class', 'badge badge-success');
    } else {
        document.getElementById(id).innerText = 'Disconnected';
        document.getElementById(id).setAttribute('class', 'badge badge-danger');
    }
}

function getCompletionTimeForAmlRequest(url, elementId, requestId, retryLimit, retryCount) {
    return getAmlActuals(url, elementId).then(data => {
        if (data['request_id'] === requestId) {
            return data['expiry_date'];
        } else if (retryCount < retryLimit) {
            return delay(100).then(
                () => getCompletionTimeForAmlRequest(
                    url, elementId, requestId, retryLimit, retryCount + 1));
        }
    });
}

function getAmlActuals(url, elementId) {
    let connectionId = elementId + '_connect_status';
    let errorId = elementId + '_error_status';
    let busyId = elementId + '_busy_status';
    let requestId = elementId + '_request_id';
    let firstMotorId = elementId + '_first';
    let secondMotorId = elementId + '_second';

    return fetch(url + '/actuals')
        .then(response => {
            setConnected(connectionId, true);
            return response.json();
        })
        .then(data => {
            getEl(firstMotorId).innerText =
                data['motor1']['position_real_world'];
            getEl(secondMotorId).innerText =
                data['motor2']['position_real_world'];
            getEl(requestId).innerText = data['request_id'];

            if (data['error_status'] !== 'Success') {
                collapsableError(errorId, data['error_status']);
            } else {
                getEl(errorId).innerHTML = '';
            }
            updateSpinnerVisbility(busyId, data);
            return data;
        })
        .catch(error => {
            setConnected(connectionId, false);
            collapsableError(errorId, error);
            getEl(firstMotorId).innerText = '-';
            getEl(secondMotorId).innerText = '-';
            getEl(requestId).innerText = '-';
        });
}

let caenAcquisitionState;
let caenListDataState;

function getCaenActuals(url, element) {
    let connectionEl = element + '_connect_status';
    let errorEl = element + '_error_status';
    let requestEl = element + '_request_id';
    let histogramNameEl = element + "_histogram_id";
    let listDataEl = element + "_list_data_id";
    let acquiringDataEl = element + "_acquiring_data";
    let acquiringDataButtonEl = element + "_toggle_acquisition";
    let listDataButtonEl = element + "_toggle_list_data";

    return fetch(url + '/actuals')
        .then(response => {
            setConnected(connectionEl, true);
            return response.json();
        })
        .catch(() => {
            setConnected(connectionEl, false);
        })
        .then(data => {
            getEl(requestEl).innerText = data['request_id'];
            getEl(histogramNameEl).innerText = data['histogram']['location'];
            getEl(listDataEl).innerText = data['list_data']['location'];
            getEl(acquiringDataEl).innerText = data['acquiring_data'];

            caenAcquisitionState = data['acquiring_data'];
            setButtonOnOrOff(acquiringDataButtonEl, caenAcquisitionState, "Acquisition started", "Acquisition stopped");

            caenListDataState = data['list_data']['storing'];
            setButtonOnOrOff(listDataButtonEl, caenListDataState, "Saving list data", "Not saving list data");

            if (data['error_status'] !== 'Success') {
                collapsableError(errorEl, data['error_status']);
            } else {
                getEl(errorEl).innerHTML = '';
            }
        })
        .catch(error => {
            collapsableError(errorEl, error);
            getEl(requestEl).innerText = '-';
            getEl(histogramNameEl).innerText = '-';
            getEl(listDataEl).innerText = '-';
            getEl(acquiringDataEl).innerText = '-';
        });
}

async function sendRequestWithExpiryDate(url, request, elementId) {
    let requestId = getUniqueIdentifier();
    let fullRequest = 'request_id=' + requestId + '\n';
    fullRequest += request;

    let requestStatusId = elementId + '_request_status';
    postData(url + '/engine', fullRequest);
    let expiry_date = await getCompletionTimeForAmlRequest(url, elementId, requestId, 10, 0);
    if (expiry_date !== undefined) {
        collapsableSucess( requestStatusId,
            'Request sent with id: ' + requestId +
            ', should be done at: ' + expiry_date);
    }
}

async function sendRequest(url, request, elementId) {
    let requestId = getUniqueIdentifier();
    let fullRequest = 'request_id=' + requestId + '\n';
    fullRequest += request;
    postData(url + '/engine', fullRequest);
    let requestStatusEl = elementId + '_request_status';
    collapsableNotify(requestStatusEl, "Sent request: " + fullRequest);
    // todo await response with correct request id ?
}

function getUniqueIdentifier() {
    // TODO: Check existing hta for javascript to generate timestamp
    let timestamp = new Date(Date.now()).toLocaleTimeString('nl-BE');
    return timestamp;
}

function collapsableNotify(id, message) {
    let notifyDiv = makeAlert('alert-secondary', message);
    document.getElementById(id).appendChild(notifyDiv);
    setTimeout(function() {
        document.getElementById(id).removeChild(notifyDiv);
    }, 5000);
}

function collapsableError(id, message) {
    getEl(id).innerHTML = '';
    let errorDiv = makeAlert('alert-danger', message);
    document.getElementById(id).appendChild(errorDiv);
}

function collapsableSucess(id, message) {
    getEl(id).innerHTML = '';
    let successDiv = makeAlert('alert-success', message);
    document.getElementById(id).appendChild(successDiv);
    setTimeout(function() {
        document.getElementById(id).removeChild(successDiv);
    }, 5000);
}

function toggleCaenAcquisitionState(elementId) {
    caenAcquisitionState = !caenAcquisitionState;

    if (caenAcquisitionState) {
        let request = "start_acquisition=true";
        sendRequest(dataAcq.caenUrl, request, 'caen');
    }
    else {
        let request = "stop_acquisition=true";
        sendRequest(dataAcq.caenUrl, request, 'caen');
    }

    let buttonId = elementId + "_toggle_acquisition";
    setButtonOnOrOff(buttonId, caenAcquisitionState, "Acquisition started", "Acquisition stopped");
}

function toggleCaenListDataState(elementId) {
    caenListDataState = !caenListDataState;
    let buttonId = elementId + "_toggle_list_data";
    setButtonOnOrOff(buttonId, caenListDataState, "Saving list data", "Not saving list data");
}

function setButtonOnOrOff(id, isOn, textOn, textOff) {
    let button = getEl(id);
    if (isOn) {
        button.innerText = textOn;
        button.classList.remove("btn-secondary");
        button.classList.add("btn-primary");
        button.classList.add("active");
    }
    else {
        button.innerText = textOff;
        button.classList.remove("btn-primary");
        button.classList.remove("active");
        button.classList.add("btn-secondary");
    }
}

function makeAlert(alertType, message) {
    let alertDiv = document.createElement('div');
    alertDiv.classList.add(
        'alert', alertType, 'alert-dismissible', 'top-margin');
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerText = message;
    let closeDiv = document.createElement('button');
    closeDiv.classList.add('close');
    closeDiv.setAttribute('data-dismiss', 'alert');
    let spanDiv = document.createElement('span');
    spanDiv.setAttribute('aria-hidden', 'true');
    spanDiv.innerHTML = '&times';
    closeDiv.append(spanDiv);
    alertDiv.append(closeDiv);

    return alertDiv;
}

function getEl(element) {
    return document.getElementById(element);
}
