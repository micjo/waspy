export {
    collapsableError,
    getUniqueIdentifier,
};

export {getEl};
export {setButtonOn, setButtonOff};
export {setConnected, setBadgeState};
export {delay};
export {postData};
export {sendRequestAndSpin, getStatus, addBadge, sendRequest};

export {hide, show};

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

function setConnected(id, connected) {
    if (connected) {
        document.getElementById(id).innerText = 'Running';
        document.getElementById(id).setAttribute(
            'class', 'badge bg-success');
    } else {
        document.getElementById(id).innerText = 'Not running';
        document.getElementById(id).setAttribute('class', 'badge bg-danger');
    }
}

function setBadgeState(id, errored) {
    if (errored) {
        getEl(id).setAttribute('class', 'badge bg-danger');
    }
    else {
        getEl(id).setAttribute('class', 'badge bg-success');
    }
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

function collapsableError(id, message) {
    getEl(id).innerHTML = '';
    let errorDiv = document.createElement('div');
    errorDiv.classList.add('alert', 'alert-danger', 'alert-dismissible', 'show');
    errorDiv.setAttribute('role', 'alert');
    errorDiv.innerText = message;
    let closeButton = document.createElement("button");
    closeButton.classList.add('btn-close');
    closeButton.setAttribute("type","button");
    closeButton.setAttribute("data-bs-dismiss","alert");
    closeButton.setAttribute("aria-label","Close");
    errorDiv.appendChild(closeButton);
    getEl(id).appendChild(errorDiv);
}

function setButtonOn(id) {
    let button = getEl(id);
    button.classList.remove("btn-secondary");
    button.classList.add("btn-primary");
    button.classList.add("active");
}

function setButtonOff(id) {
    let button = getEl(id);
    button.classList.remove("btn-primary");
    button.classList.remove("active");
    button.classList.add("btn-secondary");
}

function hide(element) {
    getEl(element).setAttribute("style", "display:none");
}

function show(element) {
    getEl(element).setAttribute("style", "display:inline-block");
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
        .then(response => response.json())
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

async function sendRequestAndSpin(url, request, spinnerId) {
    show(spinnerId);
    let data = await sendRequest(url, request);
    hide(spinnerId);
    return data
}

async function sendRequest(url, request) {
    let requestId = { "request_id" : getUniqueIdentifier()}

    let fullRequest = {
        ...requestId,
        ...request
    };
    await postData(url, JSON.stringify(fullRequest));
    let data = await waitForCompleted(url, requestId["request_id"], 50, 0);
    return data
}


async function addBadge(text, parentId) {

    let rootDiv = document.createElement('h5');
    let badgeDiv = document.createElement('span');
    badgeDiv.classList.add('badge', 'bg-success');
    badgeDiv.innerText = text;

    rootDiv.appendChild(badgeDiv);

    getEl(parentId).appendChild(rootDiv);
}

