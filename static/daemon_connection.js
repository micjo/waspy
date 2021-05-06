export {getEl,getStatus};
export {setBadgeError, setBadgeSuccess, setBadgeDanger, setText,setBadgeErrorWithText, setBadgeType};
export {sendRequestAndSpin, sendRequest, showFailureModal};

export {
    sendInt,
    sendFloat,
    sendString,
    sendARequest,
    setElementText,
    setElementChecked,
    toggle,
    show,
    hide,
};

async function postData(host, textBody) {
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

function setBadgeErrorWithText(id, success, text) {
    if (success) {
        document.getElementById(id).innerText = text;
        document.getElementById(id).setAttribute(
            'class', 'badge bg-success');
    } else {
        document.getElementById(id).innerText = text;
        document.getElementById(id).setAttribute('class', 'badge bg-danger');
    }
}

function setText(id, text) {
    getEl(id).innerText = text;
}

function setBadgeType(id, bootstrapBadgeType) {
    if (getEl(id) === null) {
        return;
    }
    getEl(id).setAttribute('class', 'badge ' + bootstrapBadgeType);
}

function setBadgeError(id, errored) {
    if (errored) {
        getEl(id).setAttribute('class', 'badge bg-danger');
    }
    else {
        getEl(id).setAttribute('class', 'badge bg-success');
    }
}

function setBadgeSuccess(id) {
    getEl(id).setAttribute('class', 'badge bg-success');
}

function setBadgeDanger(id) {
    getEl(id).setAttribute('class', 'badge bg-danger');
}

function getUniqueIdentifier() {
    // format: YYYY.MM.DD__HH:MM__SS
    let date = new Date().toISOString();
    date = date.slice(0,-5);
    date = date.split(':');

    let yearAndHour = date[0].replace(/-/g,".").replace(/T/g, "__");
    let identifier = yearAndHour +  ":" + date[1] + "__" + date[2];
    return identifier;
}


function hide(element) {
    if (getEl(element) === null) {return; }
    getEl(element).setAttribute("style", "display:none");
}

function show(element) {
    if (getEl(element) === null) {return; }
    getEl(element).setAttribute("style", "display:inline-block");
}

function disable(buttonId){
    getEl(buttonId).disabled=true;
}

function enable(buttonId){
    getEl(buttonId).disabled=false;
}

function getEl(element) {
    return document.getElementById(element);
}


async function getStatus(url) {
    let dataFromDm;
    await fetch(url)
        .then(response => response.json())
        .then(data => { dataFromDm = data; });
    return dataFromDm;
}

async function waitForCompleted(url, requestId, retryLimit, retryCount) {
    return fetch(url)
        .then(response => {
            if (response.status == 404) { throw 'Daemon not reachable.'; }
            return response.json();
        })
        .then(data => {
            if (data['request_id'] == requestId && data['request_finished'] == true) {
                return data;
            }
            else {
                if (retryCount < retryLimit) {
                return delay(250)
                .then( () => waitForCompleted(url, requestId, retryLimit, retryCount +1));
                }
            }
        });
}

async function sendRequestAndSpin(url, prefix, id, request) {

    let spinnerId = prefix + "_" + id + "_spinner";
    let clickId = prefix + "_" + id + "_click";
    show(spinnerId);
    disable(clickId);

    let data = await sendRequest(url, request);
    hide(spinnerId);
    enable(clickId);
    return data
}

async function sendRequest(url, request) {
    let requestId = { "request_id" : getUniqueIdentifier()}

    let fullRequest = {
        ...requestId,
        ...request
    };
    await postData(url, JSON.stringify(fullRequest));
    let data = await waitForCompleted(url, requestId["request_id"], 50, 0)
        .catch(error => {
            showFailureModal(error);
        });
    return data
}


function showFailureModal(text){
    var myModal = new bootstrap.Modal(document.getElementById('modalFail'))
    getEl("modalFailBody").innerText = text;
    myModal.show()
}


function sendARequest(url, prefix, id ,request) {
    let jsonRequest = JSON.parse(request);
    return sendRequestAndSpin(url,prefix, id, jsonRequest);
}

function sendInt(url,prefix, id, requestKey) {
    let value = parseInt(getEl(prefix + "_" +id + "_request").value);
    if (!Number.isInteger(value)) {
        showFailureModal('This is not a valid integer number.');
        return;
    }
    let request = {};
    request[requestKey] = value;
    return sendRequestAndSpin(url,prefix, id, request);
}

function sendString(url,prefix, id, requestKey) {
    let value = getEl(prefix + "_" +id + "_request").value;
    if (value === "Choose...") { return; }
    let request = {};
    request[requestKey] = value;
    return sendRequestAndSpin(url,prefix, id, request);
}

function sendFloat(url,prefix, id, requestKey) {
    let value = parseFloat(getEl(prefix + "_" +id + "_request").value);
    if (isNaN(value)) {
        showFailureModal("This is not a valid floating point number");
        return;
    }
    let request = {};
    request[requestKey] = value;
    return sendRequestAndSpin(url,prefix, id, request);
}

async function toggle(url, prefix, id, requestKey) {
    let value = getEl(prefix + "_" +id + "_click").checked;
    let request = {};
    request[requestKey] = value;
    return sendRequestAndSpin(url,prefix, id, request);
}


function setElementText(id, value) {
    if (getEl(id) === null) {
        return;
    }

    if (value === undefined) {
        getEl(id).innerText = "-";
    }
    else if (value === "") {
        getEl(id).innerText = "-";
    }
    else {
        getEl(id).innerText = value;
    }
}

function setElementChecked(id, checked) {
    if (getEl(id) === null) {
        return;
    }
    getEl(id).checked = checked;
}
