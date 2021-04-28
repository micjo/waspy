export {getEl,getStatus};
export {setBadgeState, setBadgeSuccess, setBadgeDanger, setText,setBadgeStateWithText};
export {sendRequestAndSpin, sendRequest, showFailureModal};

export {
    sendInt,
    sendFloat,
    sendString,
    sendARequest,
    updateElement,
    toggle
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

function setBadgeStateWithText(id, success, text) {
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

function setBadgeState(id, errored) {
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
    let date = new Date();

    // 0 + with slice(-2) ensures you have a leading 0 if needed
    let year = date.getFullYear();
    let month = ("0" + date.getMonth() + 1).slice(-2);
    let day = ("0" + date.getDay() + 1).slice(-2);

    let hours = ("0" + date.getHours()).slice(-2);
    let minutes = ("0" + date.getMinutes()).slice(-2);
    let seconds = ("0" + date.getSeconds()).slice(-2);

    let timestamp = year + "." + month + "." + day + "__" + hours + ":" + minutes + "__" + seconds;

    return timestamp;
}


function hide(element) {
    getEl(element).setAttribute("style", "display:none");
}

function show(element) {
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
    let jsonRequest =  JSON.parse(request);
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

function updateElement(id, value) {
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
