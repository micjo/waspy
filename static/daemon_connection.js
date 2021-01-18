export {
    collapsableError,
    collapsableNotify,
    collapsableSucess,
    getUniqueIdentifier,
};

export {getEl};
export {dataAcq, motors};
export {setButtonOn, setButtonOff};
export {setConnected};
export {delay};
export {postData};

export {hide, show};

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
