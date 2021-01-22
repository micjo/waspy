export {
    collapsableError,
    getUniqueIdentifier,
};

export {getEl};
export {setButtonOn, setButtonOff};
export {setConnected, setBadgeState};
export {delay};
export {postData};

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

function hide(element) {
    getEl(element).setAttribute("style", "display:none");
}

function show(element) {
    getEl(element).setAttribute("style", "display:inline-block");
}

function getEl(element) {
    return document.getElementById(element);
}
